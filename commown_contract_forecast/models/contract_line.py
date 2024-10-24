from odoo import _, api, models

from odoo.addons.queue_job.job import identity_exact


class ContractLine(models.Model):

    _inherit = "contract.line"

    @api.multi
    def _prepare_contract_line_forecast_period(
        self, period_date_start, period_date_end, recurring_next_date
    ):
        """Take contract variable discounts into account

        This requires special care for cooperative campaigns to avoid lots of http
        requests: the last generated invoice line result for the coop campaign
        discount applicability is reused.

        """
        values = super()._prepare_contract_line_forecast_period(
            period_date_start,
            period_date_end,
            recurring_next_date,
        )

        # Forecast the applicability of cooperative-campaign discounts based on
        # their results on their last generated invoice line:
        bypass_coop_campaigns = self.last_invoice_cooperative_discount_state()

        # Compute all discounts and apply them to the forecast:
        discount_values = self.with_context(
            bypass_coop_campaigns=bypass_coop_campaigns
        ).compute_discount(period_date_start)

        values["discount"] = discount_values["total"]
        if discount_values["discounts"]:
            values["name"] += "\n" + (
                _("Applied discounts:\n- %s")
                % "\n- ".join(d.name for d in discount_values["discounts"])
            )

        return values

    @api.model
    def _get_forecast_update_trigger_fields(self):
        result = super()._get_forecast_update_trigger_fields()
        result.append("specific_discount_line_ids")
        return result

    @api.multi
    def generate_forecast_periods(self, force_sync=False):
        "Don't generate forecasts when creating a contract from sale in product_rental"
        if "contract_descr" not in self.env.context:
            for contract_line in self:
                if contract_line.contract_id.company_id.enable_contract_forecast:
                    if not force_sync:
                        contract_line = contract_line.with_delay(
                            identity_key=identity_exact
                        )

                    contract_line._generate_forecast_periods()
