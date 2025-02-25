{
    'name': 'Cost Estimator',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Estimate service costs',
    'description': 'Module to estimate the costs of providing services',
    'author': 'SIMI Technologies',
    'website': 'https://simitechnologies.co.ke',
    'depends': ['base'],
    'data': [
        'security/service_estimate_security.xml',
        'security/ir.model.access.csv',
        'views/service_estimate_views.xml',
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}
