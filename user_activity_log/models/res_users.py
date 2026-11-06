import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _after_session_login(self):
        """Called once the HTTP session is fully authenticated."""
        super()._after_session_login()
        try:
            http_path = ip_address = None
            try:
                from odoo.http import request
                http_path = request.httprequest.path
                ip_address = request.httprequest.remote_addr
            except Exception:
                pass
            self.env['user.activity.log'].log(
                self, 'login',
                http_path=http_path,
                ip_address=ip_address,
                description='Logged in',
            )
        except Exception:
            _logger.exception('user_activity_log: unable to log login')
