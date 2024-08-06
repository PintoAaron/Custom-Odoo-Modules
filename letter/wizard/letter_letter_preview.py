from odoo import fields, models


class LetterPreview(models.TransientModel):
    _name = "letter.letter.preview"
    _description = "Letter Preview"
    
    letter_id = fields.Many2one('letter.letter', string='Letter', required=True)
    content = fields.Html()
    is_closed = fields.Boolean()
    
    def action_download_letter(self):
        self.ensure_one()
        return self.letter_id.action_download_letter()