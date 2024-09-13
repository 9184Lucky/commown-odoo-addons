# Copyright (C) 2018 - Today: Commown (https://commown.fr)
# @author: Florent Cayré
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Payment Slimpay issue",
    "category": "Website",
    "version": "12.0.1.0.5",
    "author": "Commown SCIC SAS",
    "license": "AGPL-3",
    "website": "https://commown.coop",
    "depends": [
        "account_payment_partner",
        "account_payment_slimpay",
        "base_automation",
        "commown_res_partner_sms",
        "project",
        "queue_job",
    ],
    "data": [
        "data/mail_template.xml",
        "data/project.xml",
        "data/product.xml",
        "data/cron.xml",
        "data/action.xml",
        "data/res_partner.xml",
        "views/project_task.xml",
    ],
    "installable": True,
}
