{
    'name': 'Letter Management',
    'version': "17.0.1.0.0",
    'application': True,
    'auto_install': False,
    'installable': True,
    'summary': 'Manage your letters',
    'description': 'A module to manage your letters',
    'license': 'LGPL-3',
    'sequence': 15,
    'author': 'Pinto T. Aaron',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/letterview.xml',
    ],
    
}