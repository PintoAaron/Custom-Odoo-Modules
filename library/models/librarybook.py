from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    title = fields.Char(string='Title', required=True)
    author_id = fields.Many2one('library.user', string='Author',
                                domain=[('user_type', '=', 'author')])
    publication_date = fields.Date(string='Publication Date', default=fields.Date.today)
    isbn = fields.Char(string='ISBN')
    description = fields.Text(string='Description')
    book_file = fields.Binary(string='Upload Book', attachment=True, help="Upload the book file here.")
    
    
    def __str__(self) -> str:
        return self.title
