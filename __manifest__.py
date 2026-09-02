{
    'name': 'Integration With Telegram',
    'version': '19.0.1.0.0',
    'author': 'Wai Phyo Htet',
    'description': """
    This Module is used to create new CRM lead For Odoo
    """,
    'license': 'LGPL-3',
    'depends': ['crm', 'base','bus'],
    'data': [
        'security/ir.model.access.csv',
        'views/social_account.xml',
        'views/customer_account_identity.xml',
        'views/menu.xml',
        'views/res_partner_inherit.xml',
    ],

    # 'assets' : {
    #     'web.assets_backend' : [
    #         'integration_with_social_platform/static/src/js/bus.js'
    #     ]
    # },
    'images' : ['static/description/icon.png'],
    'installable': True,
    'application': True,
}