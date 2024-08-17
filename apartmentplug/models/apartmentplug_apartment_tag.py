from odoo import fields, models, tools, api


class ApartmentPlugApartmentTag(models.Model):
    _name = "apartmentplug.apartment.tag"
    _description = "apartmentplug apartment tag"
    
    
    name = fields.Char(
            required=True,
            copy=False,
            string="Tag Name")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)