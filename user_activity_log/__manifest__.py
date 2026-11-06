{
    'name': 'User Activity Log',
    'version': '20.0.1.0.0',
    'category': 'Technical',
    'summary': 'Record every user activity: login, logout, page access and data changes (create / update / delete).',
    'author': 'Derry',
    'website': 'https://github.com/derry211/odoo20',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.access.csv',
        'views/user_activity_log_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
