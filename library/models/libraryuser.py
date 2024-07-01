from odoo import models, fields


class LibraryUser(models.Model):
    _name = 'library.user'
    _description = 'Library User'

    _library_user_types = [('reader', 'Reader'), ('author', 'Author')]

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    user_type = fields.Selection(selection=_library_user_types,
                                 string='User Type',
                                 required=True)
    
    
    
    def __str__(self) -> str:
        return self.name