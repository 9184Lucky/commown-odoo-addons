from odoo import api, fields, models


class ProductServiceStorableConfig(models.Model):
    _name = "product.service_storable_config"
    _description = "Describe which storable products comes with a service"

    service_tmpl_id = fields.Many2one(
        "product.template",
        string="Configured product template",
        required=True,
        domain=[("type", "=", "service")],
    )

    storable_type = fields.Selection(
        [
            ("primary", "Primary product"),
            ("secondary", "Secondary product"),
        ],
        string="Is storable primary or secondary",
        help="Does current config concern the primary storable or the secondary storables of current product variants ?",
        required=True,
    )

    attribute_value_ids = fields.Many2many(
        "product.attribute.value",
        string="Restrict to variants with following attribute values",
        required=False,
    )

    storable_tmpl_id = fields.Many2one(
        "product.template",
        required=True,
        domain=[("type", "=", "product")],
    )

    storable_variant_id = fields.Many2one(
        "product.product",
        required=True,
        domain=(
            "[('type', '=', 'product')," "('product_tmpl_id', '=', storable_tmpl_id)]"
        ),
    )

    @api.onchange("service_tmpl_id")
    def onchange_service_tmpl_id(self):
        value_ids = self.service_tmpl_id.mapped("attribute_line_ids.value_ids").ids
        return {"domain": {"attribute_value_ids": [("id", "in", value_ids)]}}
