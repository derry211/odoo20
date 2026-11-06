import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)

# Only "page" style GET requests are logged; RPC calls and static assets are not.
# Trailing slashes matter: '/web/' must not match '/websocket'.
PAGE_PREFIXES = ('/odoo', '/web/', '/mail/', '/my/')
SKIP_PREFIXES = (
    '/web/assets',
    '/web/image',
    '/web/content',
    '/web/static',
    '/web/cache',
    '/web/favicon',
    '/web/login',
    '/web/session',
    '/web/database',
    '/web/webclient',
)


def _current_env():
    """Return the current request environment, or ``None`` when there is no
    bound HTTP request."""
    try:
        if request and request.db:
            return request.env
    except Exception:
        pass
    return None


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls, endpoint):
        result = super()._dispatch(endpoint)
        cls._activity_log_access()
        return result

    @classmethod
    def _activity_log_access(cls):
        env = _current_env()
        if not env or not env.uid:
            return
        try:
            if not env['ir.config_parameter'].sudo().get_bool('user_activity_log.log_access', True):
                return
            httprequest = request.httprequest
            if httprequest.method != 'GET':
                return
            path = httprequest.path
            if not path.startswith(PAGE_PREFIXES) or path.startswith(SKIP_PREFIXES):
                return
            env['user.activity.log'].log(
                env.user, 'access',
                http_path=path,
                ip_address=httprequest.remote_addr,
                description=f'Opened {path}',
            )
        except Exception:
            _logger.exception('user_activity_log: unable to log page access')

    @classmethod
    def _post_logout(cls):
        super()._post_logout()
        # `request.env` still holds the user that is logging out: the session is
        # cleared before this hook is called, not the environment.
        env = _current_env()
        if not env or not env.uid:
            return
        try:
            httprequest = request.httprequest
            env['user.activity.log'].log(
                env.user, 'logout',
                http_path=httprequest.path,
                ip_address=httprequest.remote_addr,
                description='Logged out',
            )
        except Exception:
            _logger.exception('user_activity_log: unable to log logout')
