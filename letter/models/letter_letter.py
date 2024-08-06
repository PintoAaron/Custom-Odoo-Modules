import random
import base64
from weasyprint import HTML
from odoo import api, fields, models, tools
from odoo.tools import format_datetime
from datetime import datetime


class Letter(models.Model):
    _name = "letter.letter"
    _inherit = [
        "pipeline.record.mixin",
        "mail.tracking.duration.mixin",
    ]
    _description = "Letter"
    _track_duration_field = "stage_id"

    def _default_stage_id(self):
        letter_type_id = (
            self.env.context.get(
                "letter_type_id", False) or self.letter_type_id.id
        )
        return self.env["letter.type.stage"].search(
            [("letter_type_id", "=", letter_type_id)], limit=1
        )

    def _get_default_mail_template(self):
        letter_type = self.env.context.get("letter_type_id", False)
        if letter_type:
            letter_type = self.env["letter.type"].browse(letter_type)
            return letter_type.mail_template_id.id
        return False

    def _get_letter_templates(self):
        letter_type = self.env.context.get("letter_type_id", False)
        if letter_type:
            letter_type = self.env["letter.type"].browse(letter_type)
            return letter_type.mail_template_id.ids + letter_type.mail_template_ids.ids
        return False

    def _create_unique_reference(self, date=None):
        company = self.env.company
        date =  datetime.strptime(date, "%Y-%m-%d").date() or fields.Date.today()
        letter_count = self.env['letter.letter'].search_count(
            [('company_id', '=', company.id)])
        company_initials = "".join([word[0] for word in company.name.split()])
        formatted_date = date.strftime("%d%b%Y").upper()
        return f"{company_initials}/{formatted_date}/{letter_count+1:03d}"

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env["letter.type.stage"].search(
            [("letter_type_id", "=", stages.letter_type_id.id)],
            order=order,
        )

    def _get_default_color(self):
        return random.randint(1, 11)

    # Request fields
    name = fields.Char(
        default="/",
        index="trigram",
        string="Reference",
    )
    date = fields.Date(default=fields.Date.today)
    user_id = fields.Many2one(
        string="Author",
        default=lambda self: self.env.user,)
    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="letter_partner_rel",
        column1="letter_id",
        column2="partner_id",
        string="Recipients",
    )
    summary = fields.Char(index="trigram")
    content = fields.Html()
    color = fields.Integer(default=lambda self: self._get_default_color())
    letter_type_id = fields.Many2one(
        comodel_name="letter.type",
        string="Letter Type",
        required=True,
        ondelete="restrict",
    )
    letter_type_image = fields.Binary(related="letter_type_id.image")

    letter_type_template_ids = fields.Many2many(
        comodel_name="mail.template",
        help="Technical field for template domain",
        default=lambda self: self._get_letter_templates(),
    )

    mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        domain="[('id', 'in', letter_type_template_ids)]",
        string="Template",
        default=lambda self: self._get_default_mail_template(),
    )

    # Letter fields
    active = fields.Boolean(default=True)
    stage_id = fields.Many2one(
        comodel_name="letter.type.stage",
        copy=False,
        default=lambda self: self._default_stage_id(),
        domain="[('letter_type_id', '=', letter_type_id)]",
        group_expand="_read_group_stage_ids",
        index=True,
        ondelete="restrict",
        tracking=True,
        string="Stage",
    )

    company_id = fields.Many2one(
        string="Company",
        store=True,
        readonly=True,
        index=True,
        default=lambda self: self.env.company,
    )

    attachment_number = fields.Integer(
        "Number of Attachments", compute="_compute_attachment_number"
    )
    is_closed = fields.Boolean(compute="_compute_is_closed")

    def _compute_attachment_number(self):
        domain = [("res_model", "=", "letter.letter"),
                  ("res_id", "in", self.ids)]
        attachment_data = self.env["ir.attachment"]._read_group(
            domain, ["res_id"], ["__count"]
        )
        attachment = dict(attachment_data)
        for record in self:
            record.attachment_number = attachment.get(record.id, 0)

    def _compute_is_closed(self):
        for record in self:
            record.is_closed = record.stage_id.is_closing

    @api.onchange("letter_type_id", "partner_ids", "mail_template_id", "date")
    def _onchange_render_content(self):
        ir_qweb = self.env["ir.qweb"]
        letter_type = self.letter_type_id
        mail_template = self.mail_template_id
        if letter_type and mail_template.body_type == "qweb_view":
            body = ir_qweb._render(
                mail_template.body_view_id.id,
                {
                    "object": self,
                    "email_template": mail_template,
                    "format_datetime": lambda dt, tz=False, dt_format=False, lang_code=False: format_datetime(
                        self.env, dt, tz, dt_format, lang_code
                    ),
                },
            )
            body_html = tools.ustr(body)
            self.content = body_html

    @api.model_create_multi
    def create(self, values_list):
        for value in values_list:
            date = value.get('date', None)
            value["name"] = self._create_unique_reference(date)
        return super().create(values_list)

    def action_open_attachments(self):
        self.ensure_one()
        res = self.env["ir.actions.act_window"]._for_xml_id(
            "base.action_attachment")
        res["domain"] = [
            ("res_model", "=", "letter.letter"),
            ("res_id", "in", self.ids),
        ]
        res["context"] = {
            "default_res_model": "letter.letter",
            "default_res_id": self.id,
        }
        return res

    def action_preview_letter(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Letter Preview',
            'view_mode': 'form',
            'res_model': 'letter.letter.preview',
            'target': 'new',
            'context': {
                'default_letter_id': self.id, 
                'default_content': self.content,
                'default_is_closed': self.is_closed,
            },
        }
        
    def add_attachment(self):
        pdf_content = HTML(string=self.content).write_pdf()
        pdf_base64 = base64.b64encode(pdf_content)
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.name}.pdf',
            'type': 'binary',
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })  
        return attachment
        

    def action_download_letter(self):
        self.ensure_one()
        attachment = self.add_attachment()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
        

   