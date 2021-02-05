{
    'name': 'Commown SCIC SAS',
    'category': 'Business',
    'summary': 'Commown SCIC SAS business application',
    'version': "12.0.1.0.0",
    'description': "Commown SCIC SAS business application",
    'author': "Commown SCIC SAS",
    'license': "AGPL-3",
    'website': "https://commown.coop",
    'depends': [
        # Commown modules
        'account_loan',
        # 'account_bank_statement_import_credit_coop',
        # 'account_bank_statement_import_lanef',
        'account_invoice_merge_auto_pay',
        # 'account_move_slimpay_import',
        'commown_shipping',
        'commown_ergonomy_asset',
        'commown_lead_risk_analysis',
        # 'contract_auto_merge_invoice',
        'website_sale_payment_slimpay',
        'payment_slimpay_issue',
        'product_rental',
        'project_rating_nps',
        'sale_product_email',
        'urban_mine',
        'custom_report',
        'website_sale_affiliate_portal',
        'website_sale_affiliate_product_restriction',
        # 'website_sale_b2b',
        'sale_promotion_rule',
        # OCA modules
        'account_payment_sale',
        'account_mass_reconcile',
        'auth_signup',
        'base_automation',
        'crm',
        'mass_mailing',
        'mass_mailing_partner',
        'project',
        'website_sale_cart_selectable',
        # 'website_sale_default_country',
        'website_sale_hide_price',
        'website_sale_require_login',
        'portal',
    ],

    'external_dependencies': {
        'python': ['magic'],
        'bin': ['rsvg-convert'],
    },

    'data': [
        'views/contract_contract_view.xml',
        'views/contract_template_view.xml',
        'views/address_template.xml',
        'views/auth_signup.xml',
        # 'views/cart.xml',
        'views/actions_sale_order.xml',
        'views/actions_account_invoice.xml',
        # 'views/product_template.xml',
        # 'views/project_issue.xml',
        # 'views/webclient_templates.xml',
        # 'views/website_portal_templates.xml',
        # 'views/website_sale_templates.xml',
        # 'views/website_site_portal_sale_templates.xml',
        'views/res_partner.xml',
        'views/crm_lead.xml',
        'data/product.xml',
        # 'data/mail_templates.xml',
        'data/project_project.xml',
    ],
    'qweb': [
        'static/src/xml/account_reconciliation.xml',
    ],
    'installable': True,
    'application': True,
}
