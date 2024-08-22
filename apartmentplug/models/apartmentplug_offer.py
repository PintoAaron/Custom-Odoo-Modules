from odoo import fields, models, tools, api
from odoo.exceptions import UserError



class ApartmentplugOffer(models.Model):
    _name = 'apartmentplug.offer'
    _description = 'apartmentplug.offer'
    
    
    
    price = fields.Float(string='Price', copy=False)
    status = fields.Selection(string='Status', selection=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),],
        readonly=True,
        default='pending')
    partner_id = fields.Many2one(
            comodel_name='res.partner', 
            string='Customer', 
            required=True)
    property_id = fields.Many2one(
        comodel_name='apartmentplug.apartment', 
        string='Apartment', 
        required=True)
    
    
    def action_accept(self):
        accepted_offer = self.env['apartmentplug.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
            ('id', '!=', self.id)])
        
        if accepted_offer:
            raise UserError('There is already an accepted offer for this property.')
            
        
        other_offers = self.env['apartmentplug.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'pending'),
            ('id', '!=', self.id)])
        
        for offer in other_offers:
            offer.status = 'refused'
        
        self.status = 'accepted'
        
        self.property_id.state = 'offer accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id

        return True
    
    
    def action_refuse(self):
        if self.status == 'accepted':
            self.property_id.state = 'offer received'
            self.property_id.selling_price = 0.0
            self.property_id.partner_id = False
        self.status = 'refused'
        return True
        

    
    
    
    
        
