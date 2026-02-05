{
    'name': 'estate',
    'version': '1.0',
    'license':'OEEL-1',
    'depends': ['base','crm','sale'],
    'application': True,
    'demo': ['demo/demo.xml',],
    'data': [

        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_sequence.xml',
        'views/assignment9.xml'
    ]
}