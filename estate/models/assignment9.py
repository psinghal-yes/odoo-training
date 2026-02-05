from odoo import fields,api,models
from odoo.exceptions import ValidationError
from datetime import date

class CRMValidation(models.Model):
    _inherit = "crm.lead"

    @api.constrains('date_deadline')
    def _check_date_validity(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_deadline and rec.date_deadline < today:
                raise ValidationError("Deadline must be today or in the future.")

class SalesInherit(models.Model):
    _inherit = "sale.order"

    total_orders = fields.Float(compute='_compute_total_orders' ,store=True)


    @api.depends('order_line.product_uom_qty')
    def _compute_total_orders(self):
        for rec in self:
            rec.total_orders = sum(rec.order_line.mapped('product_uom_qty'))
