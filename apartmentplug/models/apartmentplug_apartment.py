from odoo import fields, models, tools, api
from datetime import timedelta


class ApartmentPlugApartment(models.Model):
    _name = "apartmentplug.apartment"
    _description = "apartmentplug apartment"
    
    
    def _get_default_availability_date(self):
        return fields.Date.today() + timedelta(months=3)
    
    
    name = fields.Char(
                required=True,
                default="Unknown",
                copy=False,
                index=True,
                help="Name of the apartment",
                string="Apartment Name")
    property_type_id = fields.Many2one(
                comodel_name="apartmentplug.property.type",
                string="Property Type",
                required=True)      
    user_id = fields.Many2one(
                comodel_name="res.partner",
                string="Seller",
                required=True,
                domain=[('is_company', '=', False)],
                copy=False,
                index=True,
                help="Owner of the apartment",
                default=lambda self: self.env.user)
    partner_id = fields.Many2one(
                comodel_name="res.partner",
                string="Buyer",
                domain=[('is_company', '=', False)],
                copy=False,
                index=True)
    description = fields.Text()
    tags_ids = fields.Many2many(
                comodel_name="apartmentplug.apartment.tag",
                string="Tags")
    postcode = fields.Char()
    date_availability = fields.Date(
                        default=fields.Date.today,
                        copy=False,
                        string="Available From")
    expected_price = fields.Float(default=0.00,string="Expected Price")
    selling_price = fields.Float(readonly=True, 
                                 copy=False, 
                                 string="Selling Price")
    bedrooms = fields.Integer(default=2,string="Bedrooms")
    living_rooms = fields.Integer(default=1,string="Living Rooms")
    facades = fields.Integer(default=0,string="Facades")
    garage = fields.Boolean(default=False,string="Garage")
    garden = fields.Boolean(default=False,string="Garden")
    garden_area = fields.Integer(default = 0,string="Garden Area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'),('west', 'West'), ('south', 'South')],
        help="The direction in which the garden is facing")
    state = fields.Selection(
        string='Status',
        required=True,
        selection=[('new', 'New'),('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'),('sold', 'Sold'),
                   ('canceled','Canceled')],
        default="new",
        copy=False
    )
    active = fields.Boolean(default=True)