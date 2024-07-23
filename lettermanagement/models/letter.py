from odoo import models, fields


class LetterManagementLetter(models.Model):
    _name = 'lettermanagement.letter'
    _description = 'Letter Management Letter'

    owner = fields.Many2one('res.partner', string='Owner', required=True)
    letter = fields.Many2one('mail.template', string='Letter', required=True)