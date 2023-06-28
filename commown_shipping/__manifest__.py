{
    "name": "Commown shipping",
    "category": "Business",
    "summary": "Commown shipping-related features",
    "version": "12.0.1.0.8",
    "author": "Commown SCIC,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://commown.coop",
    "depends": [
        "base_automation",
        "sale",
        "website",
        "crm",
        "partner_firstname",
        "project",
        "queue_job",
        "server_environment",
        "web_ir_actions_act_multi",
    ],
    "external_dependencies": {
        "bin": ["pdfjam", "pdftk"],
        "python": ["requests_toolbelt"],
    },
    "data": [
        "data/actions.xml",
        "data/cron.xml",
        "data/mail_template.xml",
        "data/parcels.xml",
        "data/shipping_accounts.xml",
        "views/crm_team.xml",
        "views/crm_lead.xml",
        "views/parcels.xml",
        "views/product.xml",
        "views/project_project.xml",
        "views/project_task.xml",
        "views/wizard_print_label.xml",
        "security/ir.model.access.csv",
    ],
    "demo": ["data/demo.xml"],
    "installable": True,
}
