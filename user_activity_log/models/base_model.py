import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)

LOG_MODEL = 'user.activity.log'

# Models that never produce an activity entry: the log itself (recursion) plus
# technical/noisy models that would flood the log without adding value.
IGNORED_MODELS = frozenset({
    LOG_MODEL,
    'ir.logging',
    'ir.cron',
    'bus.bus',
    'bus.presence',
    'mail.message',
    'mail.notification',
    'mail.tracking.value',
    'mail.presence',
    'res.users.log',
    'base_registry_signaling',
    'base_cache_signaling',
})

IGNORED_WRITE_FIELDS = frozenset({'write_date', 'write_uid', '__last_update'})
MAX_RECORD_NAME = 255
MAX_FIELDS = 15


class BaseActivityLog(models.AbstractModel):
    _inherit = 'base'

    # ------------------------------------------------------------------
    # Guards
    # ------------------------------------------------------------------
    def _activity_log_enabled(self):
        """Whether an operation on ``self`` should be written to the log."""
        if self._transient or self._name in IGNORED_MODELS:
            return False
        if self.env.context.get('activity_log_skip'):
            return False
        if not self.env.registry.ready:
            # module install / update in progress
            return False
        try:
            if not request or not request.db:
                return False
        except Exception:
            # no HTTP request bound (cron, CLI, tests)
            return False
        try:
            if not self.env['ir.config_parameter'].sudo().get_bool('user_activity_log.enabled', True):
                return False
        except Exception:
            pass
        return True

    # ------------------------------------------------------------------
    # Entry building
    # ------------------------------------------------------------------
    def _activity_log_http_info(self):
        try:
            httprequest = request.httprequest
            return httprequest.path, httprequest.remote_addr
        except Exception:
            return None, None

    def _activity_log_description(self, action, record_name, vals):
        label = f'"{record_name}"' if record_name else ''
        if action == 'create':
            return f'Created {self._name} {label}'.strip()
        if action == 'unlink':
            return f'Deleted {self._name} {label}'.strip()
        changed = sorted(set(vals or {}) - IGNORED_WRITE_FIELDS)
        if not changed:
            return f'Updated {self._name} {label}'.strip()
        shown = ', '.join(changed[:MAX_FIELDS])
        extra = '' if len(changed) <= MAX_FIELDS else f' (+{len(changed) - MAX_FIELDS} more)'
        return f'Updated {self._name} {label}: {shown}{extra}'.strip()

    def _activity_log_flush(self, action, vals=None, snapshot=None):
        try:
            path, ip_address = self._activity_log_http_info()
            user = self.env.user
            if snapshot is not None:
                records = list(snapshot)
            else:
                records = [(rec.id, rec.display_name) for rec in self]
            entries = [{
                'user_id': user.id,
                'action': action,
                'model_name': self._name,
                'res_id': res_id,
                'record_name': (name or '')[:MAX_RECORD_NAME],
                'description': self._activity_log_description(action, name, vals),
                'http_path': path,
                'ip_address': ip_address,
                'user_tz': user.tz,
            } for res_id, name in records]
            if entries:
                self.env[LOG_MODEL]._create_entries(entries)
        except Exception:
            # logging must never break the underlying operation
            _logger.exception('user_activity_log: unable to write activity log')

    # ------------------------------------------------------------------
    # ORM hooks
    # ------------------------------------------------------------------
    def create(self, vals_list):
        records = super().create(vals_list)
        if records._activity_log_enabled():
            records._activity_log_flush('create')
        return records

    def write(self, vals):
        result = super().write(vals)
        if self._activity_log_enabled():
            self._activity_log_flush('write', vals=vals)
        return result

    def unlink(self):
        enabled = self._activity_log_enabled()
        snapshot = [(rec.id, rec.display_name) for rec in self] if enabled else None
        result = super().unlink()
        if enabled:
            self._activity_log_flush('unlink', snapshot=snapshot)
        return result
