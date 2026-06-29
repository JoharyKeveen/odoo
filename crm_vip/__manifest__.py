{
    'name': 'CRM VIP',
    'version': '1.0',
    'summary': 'Gestion des clients VIP dans le CRM',
    'description': 'Module pour gérer les clients VIP avec des informations supplémentaires',
    'author': 'Moi',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_vip_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}