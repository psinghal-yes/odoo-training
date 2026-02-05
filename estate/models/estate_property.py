from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"

    number = fields.Char('Reference', readonly=True, copy=False,
                         default = lambda self : self.env['ir.sequence'].next_by_code('estate.property'))

    name = fields.Char(string="Property Name" ,required=True)
    description = fields.Text(string="Property Description")
    active = fields.Boolean(default=True)
    postcode = fields.Char(string="Property Postcode")
    date_availability = fields.Datetime(string="Date Availability" , copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms= fields.Integer(string="Bedrooms" ,default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")

    buyer_id = fields.Many2one("res.partner", string="Buyer" )
    salesperson_id = fields.Many2one("res.users", string="Salesperson" ,default=lambda self: self.env.user)

    property_type_id = fields.Many2one("estate.property.type","Property Type")

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')
        ],

    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new'
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")

    _sql_constraints = [
        ('check_positive_exp_price','CHECK(expected_price>=0)','Expected Price should be Positive'),
        ('check_positive_selling_price', 'CHECK(selling_price>=0)', 'Selling Price should be Positive'),
    ]




    @api.onchange('garden')
    def onchange_garden(self):
        if not self.garden:
            self.garden = 0
            self.garden_orientation = None

    def sold_action(self):
        if self.state == 'canceled':
            raise UserError("Canceled Properties cannot be Sold")
        self.state = 'sold'
        return True

    def cancel_action(self):
        if self.state == 'sold':
            raise UserError("Sold Properties cannot be Canceled")
        self.state = 'canceled'
        return True

    @api.ondelete(at_uninstall=False)
    def on_del_property(self):
        for rec in self:
            if rec.state not in ['new','canceled']:
                raise UserError("You cannot delete this property!!")


class EstatePropertyCustom(models.Model):
    _inherit = "estate.property"

    pets_allowed = fields.Boolean(string="Pet Allowed")

