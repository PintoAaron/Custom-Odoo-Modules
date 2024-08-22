from odoo import fields, models, api
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
        readonly=True,
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
    expected_price = fields.Float(default=0.00, string="Expected Price")
    selling_price = fields.Float(readonly=True,
                                 copy=False,
                                 string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Float(
        default=0.00,
        string="Living Area (sqm)",
    )
    facades = fields.Integer(default=0, string="Facades")
    garage = fields.Boolean(default=False, string="Garage")
    garden = fields.Boolean(default=False, string="Garden")
    garden_area = fields.Float(
        default=0.00,
        string="Garden Area (sqm)",
    )
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'),
                   ('west', 'West'), ('south', 'South')],
    )
    state = fields.Selection(
        string='Status',
        required=True,
        selection=[('new', 'New'), ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
                   ('canceled', 'Canceled')],
        compute='_compute_state',
        copy=False
    )
    total_area = fields.Float(
        string='Total Area (sqm)',
        readonly=True,
        compute='_compute_total_area',
    )
    best_offer = fields.Float(
        string='Best Offer',
        readonly=True,
        compute='_compute_best_offer',
    )
    offer_ids = fields.One2many(
        comodel_name="apartmentplug.offer",
        inverse_name="property_id",
        string="Offers")
    active = fields.Boolean(default=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(
                    [item.price for item in record.offer_ids])
            else:
                record.best_offer = 0.0

    @api.depends('offer_ids','partner_id')
    def _compute_state(self):
        for record in self:
            if record.partner_id:
                record.state = "sold"
            elif record.offer_ids:
                record.state = "offer received"
            else:
                record.state = "new"

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.00
            self.garden_orientation = 'south'
        else:
            self.garden_area = 0.00
            self.garden_orientation = ''

    # @api.onchange('offer_ids')
    # def _onchange_offer_ids(self):
    #     if self.offer_ids:
    #         accepted_offer = self.offer_ids.filtered(
    #             lambda x: x.status == 'accepted')
    #         if accepted_offer:
    #             self.state = 'offer accepted'
    #             self.selling_price = accepted_offer.price
    #             self.partner_id = accepted_offer.partner_id
    #         else:
    #             self.state = 'offer received'
    #     else:
    #         self.state = 'new'
            
        
