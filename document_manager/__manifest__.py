{
    'name': 'Document Manager Ext',
    'version': '14.0.0.0',
    'application': True,
    'auto_install': False,
    'installable': True,
    'summary': 'help u edit ur documents',
    'description': 'document management made easier',
    'license': 'LGPL-3',
    'sequence': 15,
    'author': 'Mac quena',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/document.xml',
    ],
    
}