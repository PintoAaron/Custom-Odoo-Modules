from odoo import fields, models, tools, api


class ApartmentPlugPropertyType(models.Model):
    _name = "apartmentplug.property.type"
    _description = "apartmentplug property type"
    
    
    name = fields.Char(
            required=True,
            copy=False,
            string="Apartment Type")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)