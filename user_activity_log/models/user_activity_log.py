import logging
from datetime import timedelta
from zoneinfo import ZoneInfo

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

UTC = ZoneInfo('UTC')


class UserActivityLog(models.Model):
    _name = 'user.activity.log'
    _description = 'User Activity Log'
    _order = 'id desc'
    _rec_name = 'record_name'

    user_id = fields.Many2one(
        'res.users', string='User', required=True, ondelete='cascade', index=True)
    login = fields.Char(string='Login', related='user_id.login')
    action = fields.Selection(
        selection=[
            ('login', 'Login'),
            ('logout', 'Logout'),
            ('access', 'Page Access'),
            ('create', 'Create'),
            ('write', 'Update'),
            ('unlink', 'Delete'),
        ],
        string='Action', required=True, index=True)
    model_name = fields.Char(string='Model', index=True)
    res_id = fields.Integer(string='Record ID')
    record_name = fields.Char(string='Record')
    description = fields.Text(string='Activity')
    http_path = fields.Char(string='Path')
    ip_address = fields.Char(string='IP Address')
    user_tz = fields.Char(string='Timezone')
    local_time = fields.Char(
        string='Local Time', compute='_compute_local_time')

    @api.depends('create_date', 'user_tz')
    def _compute_local_time(self):
        for log in self:
            log.local_time = self._format_local_time(log.create_date, log.user_tz)

    @api.model
    def _format_local_time(self, timestamp, tz_name):
        """Format a naive-UTC timestamp in the given timezone (the acting
        user's own timezone, falling back to the viewer's timezone)."""
        if not timestamp:
            return False
        tz_name = tz_name or self.env.user.tz or 'UTC'
        try:
            tzinfo = ZoneInfo(tz_name)
        except Exception:
            tz_name = 'UTC'
            tzinfo = UTC
        local = timestamp.replace(tzinfo=UTC).astimezone(tzinfo)
        return f"{local.strftime('%Y-%m-%d %H:%M:%S')} ({tz_name})"

    @api.model
    def log(self, user, action, **values):
        """Create a single activity log entry for ``user``."""
        if not user or not user.id:
            return self.browse()
        values.setdefault('user_tz', user.tz)
        values['user_id'] = user.id
        values['action'] = action
        return self._create_entries([values])

    @api.model
    def _create_entries(self, entries):
        # sudo + a dedicated context flag: bypass record rules and never let the
        # base create() override log the log entries themselves (no recursion).
        return self.sudo().with_context(activity_log_skip=True).create(entries)

    @api.autovacuum
    def _gc_activity_logs(self):
        """Drop entries older than ``user_activity_log.retention_days``
        (0 / unset = keep everything)."""
        days = self.env['ir.config_parameter'].sudo().get_int(
            'user_activity_log.retention_days', 0)
        if days <= 0:
            return
        limit = fields.Datetime.now() - timedelta(days=days)
        stale = self.sudo().search([('create_date', '<', limit)])
        if stale:
            _logger.info('Purging %d activity log entries older than %d days', len(stale), days)
            stale.unlink()
