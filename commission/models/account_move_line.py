from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = [
        "account.move.line",
    ]

    settlement_id = fields.Many2one(
        comodel_name="commission.settlement",
        help="Settlement that generates this invoice line",
        copy=False,
    )

    def _copy_data_extend_business_fields(self, values):
        """
        We don't want to loose the settlement from the line when reversing the line if
        it was a refund.
        We need to include it, but as we don't want change it everytime, we will add
        the data when a context key is passed
        """
        super()._copy_data_extend_business_fields(values)
        if self.settlement_id and self.env.context.get("include_settlement", False):
            values["settlement_id"] = self.settlement_id.id
        return
