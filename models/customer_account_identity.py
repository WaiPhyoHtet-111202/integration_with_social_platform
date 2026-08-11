from odoo import api, fields, models

class CustomerAccountIdentity(models.Model):
    _name = 'customer.account.identity'
    _description = 'Customer Account Identity'

    name = fields.Char(string='Name')
    platform = fields.Char(string='Platform')
    partner_id = fields.Many2one("res.partner", string='Partner')
    external_id = fields.Char(string='External ID')