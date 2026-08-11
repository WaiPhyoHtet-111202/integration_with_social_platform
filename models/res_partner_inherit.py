from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Res Partner"

    social_platform = fields.Char(
        string="Social Platform",
    )