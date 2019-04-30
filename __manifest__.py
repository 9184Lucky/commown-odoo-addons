{
    'name': 'Commown shipping',
    'category': 'Business',
    'summary': 'Commown shipping-related features',
    'version': '10.0.1.1.2',
    'description': 'Commown label printing and shipping followup',
    'author': "Commown SCIC SAS",
    'license': "AGPL-3",
    'website': "https://commown.fr",
    'depends': [
        'crm',
        'project_issue',
        'keychain',
        'partner_firstname',
    ],
    'external_dependencies': {
        'bin': ['pdfjam'],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/parcels.xml',
        'data/actions.xml',
        'data/keychain_accounts.xml',
        'views/project.xml',
        'views/team.xml',
    ],
    'installable': True,
}
