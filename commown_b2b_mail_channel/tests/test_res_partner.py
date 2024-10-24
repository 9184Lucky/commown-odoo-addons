from datetime import date

from odoo.tests.common import SavepointCase


class ResPartnerTC(SavepointCase):
    def setUp(self):
        super().setUp()
        self.company = self.env["res.partner"].create(
            {"name": "Company", "company_type": "company"}
        )

        user1 = self.env["res.users"].create({"name": "u1", "login": "u1"})
        user2 = self.env["res.users"].create({"name": "u2", "login": "u2"})

        self.part1 = user1.partner_id
        self.part2 = user2.partner_id

        self.user_support = self.env["res.users"].create(
            {"name": "Test support", "login": "login"}
        )
        self.user_support.groups_id |= self.env.ref("commown_user_groups.support")

        self.contract = self.env["contract.contract"].create(
            {"name": "Test contract", "partner_id": self.part1.id}
        )

    def test_support_channel_creation_on_contract_start(self):
        self.part1.parent_id = self.company
        self.part2.parent_id = self.company
        self.assertFalse(self.company.mail_channel_id)

        self.contract.date_start = date.today()

        company_chan = self.company.mail_channel_id
        expected_groups = self.env["res.groups"]
        for name in ["support", "commercial", "admin"]:
            expected_groups |= self.env.ref("commown_user_groups.%s" % name)

        self.assertEqual(company_chan.name, "Support %s" % self.company.name)
        self.assertEqual(
            company_chan.channel_last_seen_partner_ids.mapped("partner_id"),
            self.part1 + self.part2 + self.user_support.partner_id,
        )
        self.assertEqual(company_chan.group_ids, expected_groups)

    def test_partner_is_added_when_parent_has_channel(self):
        self.company.create_mail_channel()
        mail_channel = self.company.mail_channel_id
        self.assertTrue(mail_channel)

        initial_parts = mail_channel.channel_last_seen_partner_ids.mapped("partner_id")

        self.part1.parent_id = self.company
        self.assertEqual(
            mail_channel.channel_last_seen_partner_ids.mapped("partner_id"),
            initial_parts + self.part1,
        )

        self.part1.parent_id = False
        self.assertEqual(
            mail_channel.channel_last_seen_partner_ids.mapped("partner_id"),
            initial_parts,
        )

    def test_channel_creation_on_active_contract_join_company(self):
        """Test if channel is created when a partner with an active contract join
        company"""
        self.part2.parent_id = self.company
        self.contract.date_start = date.today()
        self.assertFalse(self.company.mail_channel_id)

        self.part1.parent_id = self.company
        self.assertTrue(self.company.mail_channel_id)

    def test_set_support_channel_name(self):
        self.company.create_mail_channel()
        self.assertEqual(
            self.company.mail_channel_id.name,
            "Support %s" % self.company.name,
        )

        new_name = "New name"

        self.company.name = new_name
        self.assertEqual(
            self.company.mail_channel_id.name,
            "Support %s" % new_name,
        )

    def test_partner_are_unsubscribed_when_company_is_changed(self):
        company_2 = self.company.copy()

        self.part1.parent_id = self.company
        self.part2.parent_id = company_2

        self.company.create_mail_channel()
        mail_channel = self.company.mail_channel_id

        self.assertIn(
            self.part1,
            mail_channel.mapped("channel_last_seen_partner_ids.partner_id"),
        )
        self.assertNotIn(
            self.part2,
            mail_channel.mapped("channel_last_seen_partner_ids.partner_id"),
        )

        mail_channel.company_id = company_2
        self.assertEquals(mail_channel.company_id, mail_channel.company_ids)
        self.assertIn(
            self.part2,
            mail_channel.mapped("channel_last_seen_partner_ids.partner_id"),
        )
        self.assertNotIn(
            self.part1,
            mail_channel.mapped("channel_last_seen_partner_ids.partner_id"),
        )
