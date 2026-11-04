{
    'name': 'ICA Web Responsive',
    'category': 'Hidden',
    'depends': ['web', 'base_setup'],
    'auto_install': ['web'],
    'data': [
        'views/webclient_templates.xml',
        'views/res_config_settings.xml',
        'views/res_users_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'web/static/src/scss/primary_variables.scss', 'ica_web_responsive/static/src/**/*.variables.scss'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'ica_web_responsive/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'web/static/src/scss/secondary_variables.scss', 'ica_web_responsive/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'ica_web_responsive/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'ica_web_responsive/static/src/webclient/home_menu/home_menu_background.scss', # used by login page
            'ica_web_responsive/static/src/webclient/navbar/navbar.scss',
        ],
        'web.assets_backend': [
            'ica_web_responsive/static/src/webclient/**/*.scss',
            'ica_web_responsive/static/src/views/**/*.scss',

            'ica_web_responsive/static/src/core/**/*',
            'ica_web_responsive/static/src/webclient/**/*.js',
            ('after', 'web/static/src/views/list/list_renderer.xml', 'ica_web_responsive/static/src/views/list/list_renderer_desktop.xml'),
            ('after', 'web/static/src/views/kanban/kanban_renderer.xml', 'ica_web_responsive/static/src/views/kanban/kanban_renderer.xml'),
            ('after', 'web/static/src/views/kanban/kanban_header.xml', 'ica_web_responsive/static/src/views/kanban/kanban_header.xml'),
            ('after', 'web/static/src/views/widgets/ribbon/ribbon.xml', 'ica_web_responsive/static/src/views/widgets/ribbon/ribbon.xml'),
            ('after', 'web/static/src/views/calendar/calendar_controller.xml', 'ica_web_responsive/static/src/views/calendar/calendar_controller.xml'),
            ('after', 'web/static/src/views/calendar/calendar_side_panel/calendar_side_panel.xml', 'ica_web_responsive/static/src/views/calendar/calendar_side_panel/calendar_side_panel.xml'),
            'ica_web_responsive/static/src/webclient/**/*.xml',
            'ica_web_responsive/static/src/views/**/*.js',
            'ica_web_responsive/static/src/views/**/*.xml',
            'ica_web_responsive/static/src/search/**/*.js',
            'ica_web_responsive/static/src/search/**/*.scss',
            ('after', '/web/static/src/search/control_panel/control_panel.xml', 'ica_web_responsive/static/src/search/control_panel/control_panel.xml'),
            ('remove', 'ica_web_responsive/static/src/views/pivot/**'),
            ('remove', 'ica_web_responsive/static/src/views/graph/**'),

            # Don't include dark mode files in light mode
            ('remove', 'ica_web_responsive/static/src/**/*.dark.scss'),
        ],
        'web.assets_backend_lazy': [
            'ica_web_responsive/static/src/views/pivot/**',
            'ica_web_responsive/static/src/views/graph/**',
        ],
        'web.assets_backend_lazy_dark': [
            ('include', 'web.dark_mode_variables'),
            # web._assets_backend_helpers
            ('before', 'ica_web_responsive/static/src/scss/bootstrap_overridden.scss', 'ica_web_responsive/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'ica_web_responsive/static/src/scss/bs_functions_overridden.dark.scss'),
        ],
        'web.assets_web': [
            ('replace', 'web/static/src/main.js', 'ica_web_responsive/static/src/main.js'),
        ],
        # ========= Dark Mode =========
        "web.dark_mode_variables": [
            # web._assets_primary_variables
            ('before', 'ica_web_responsive/static/src/scss/primary_variables.scss', 'ica_web_responsive/static/src/scss/primary_variables.dark.scss'),
            ('before', 'ica_web_responsive/static/src/**/*.variables.scss', 'ica_web_responsive/static/src/**/*.variables.dark.scss'),
            # web._assets_secondary_variables
            ('before', 'ica_web_responsive/static/src/scss/secondary_variables.scss', 'ica_web_responsive/static/src/scss/secondary_variables.dark.scss'),
        ],
        "web.assets_web_dark": [
            ('include', 'web.dark_mode_variables'),
            # web._assets_backend_helpers
            ('before', 'ica_web_responsive/static/src/scss/bootstrap_overridden.scss', 'ica_web_responsive/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'ica_web_responsive/static/src/scss/bs_functions_overridden.dark.scss'),
            # assets_backend
            'ica_web_responsive/static/src/**/*.dark.scss',
        ],
    },
    "images":["static/description/img_1.png"],
    'author': 'Agga, IdeaCode Academy',
    'license': 'LGPL-3',
}
