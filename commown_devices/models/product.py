from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    storable_product_id = fields.Many2one(
        "product.template",
        string="Storable product",
        domain='[("type", "=", "product")]',
    )

    storable_config_ids = fields.One2many(
        string="Storable configurations",
        comodel_name="product.service_storable_config",
        inverse_name="service_tmpl_id",
    )

    @api.onchange("storable_config_ids")
    def onchange_storable_config_ids(self):
        self._origin.product_variant_ids._set_storable_variants(
            self.storable_config_ids
        )

    @api.multi
    def create_variant_ids(self):
        res = super(ProductTemplate, self).create_variant_ids()
        self.product_variant_ids._set_storable_variants()
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    primary_storable_variant_id = fields.Many2one(
        "product.product",
        string="Primary storable variant",
        domain='[("type", "=", "product")]',
    )

    secondary_storable_variant_ids = fields.Many2many(
        "product.product",
        relation="secondary_variants",
        column1="service_product_id",
        column2="storable_product_id",
        string="Secondary storable variants",
        domain='[("type", "=", "product")]',
    )

    @api.multi
    def _set_storable_variants(self, template_configs=None):
        for rec in self:
            if template_configs is None:
                template_configs = rec.product_tmpl_id.storable_config_ids
            configs = template_configs.filtered(
                lambda c: set(c.attribute_value_ids.ids).issubset(
                    rec.attribute_value_ids.ids
                )
            )
            primary_variant = self.env["product.product"]
            secondary_variants = self.env["product.product"]
            for c in configs:
                if c.storable_type == "primary":
                    primary_variant |= c.storable_variant_id
                elif c.storable_type == "secondary":
                    secondary_variants |= c.storable_variant_id
            assert len(primary_variant) <= 1, _(
                "More than one primary variant configured for %s with attributes %s"
                % (rec.name, rec.attribute_value_ids.mapped("name"))
            )
            if len(secondary_variants) > len(
                secondary_variants.mapped("product_tmpl_id")
            ):
                raise Warning(
                    _(
                        "For product %s, two secondary variants derive from the same template,"
                        " are you sure that there is no configuration mistake ?"
                        % rec.name
                    )
                )
            rec.primary_storable_variant_id = primary_variant
            rec.secondary_storable_variant_ids = secondary_variants
