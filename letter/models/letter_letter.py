import random

from odoo import api, fields, models


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
    date = fields.Datetime()
    user_id = fields.Many2one(string="Author")
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
        related="letter_type_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    attachment_number = fields.Integer(
        "Number of Attachments", compute="_compute_attachment_number"
    )

    def _compute_attachment_number(self):
        domain = [("res_model", "=", "letter.letter"),
                  ("res_id", "in", self.ids)]
        attachment_data = self.env["ir.attachment"]._read_group(
            domain, ["res_id"], ["__count"]
        )
        attachment = dict(attachment_data)
        for record in self:
            record.attachment_number = attachment.get(record.id, 0)

    @api.model_create_multi
    def create(self, values_list):
        for value in values_list:
            value["name"] = self.env["ir.sequence"].next_by_code(
                "letter.letter")
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
