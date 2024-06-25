from odoo import models, fields
import random


class Property(models.Model):
    _name = 'estate.property'
    _description = 'estate property'

    _estate_owners = ['Macquena', 'Moses', 'Emma', 'Aaron', 'Jacob', 'Isaac', 'Abraham', 'Sarah', 'Rebecca', 'Rachel']

    def _generate_random_name(self):
        return random.choice(self._estate_owners)

    name = fields.Char(string='Name', required=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    selling_price = fields.Float(string='Selling Price')
    backyard = fields.Boolean(string='Backyard', help='Is there a backyard for this property')
    owner = fields.Char(string='Owner', readonly=True, default=lambda self: self._generate_random_name())
