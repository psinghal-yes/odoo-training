from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string='Price',)
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner' ,required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Offer Deadline", compute='_compute_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            # self.property_id.state = 'offer_accepted'
            raise UserError(message= "Offer Already Accepted")

        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.selling_price = self.price

    def action_reject(self):
        self.ensure_one()
        if "refused" in self.property_id.offer_ids.mapped('status'):
            raise UserError(message= "Offer Already Rejected")
        self.status = 'refused'
        self.property_id.selling_price = 0

    @api.model
    def create(self, vals_list):
        # for rec in self:
        #     max_offer_price = max(rec.property_id.offer_ids.mapped('price'))
        #     if vals_list.get('price') < max_offer_price:
        #         raise UserError(message= "Offers with lower prices than existing offers are not allowed")

        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'

        return offers

    def _cron_remove_expired_offers(self):
        today = fields.Date.today()

        expired_offers = self.search([('date_deadline', '<', today), ('status', '!=', 'accepted')])

        expired_offers.unlink()