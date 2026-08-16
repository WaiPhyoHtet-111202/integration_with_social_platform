from odoo import api, fields, models

class CustomerAccountIdentity(models.Model):
    _name = 'customer.account.identity'
    _description = 'Customer Account Identity'

    user_name = fields.Char(string='User Name')
    first_name = fields.Char(string='First Name')
    platform = fields.Char(string='Platform')
    partner_id = fields.Many2one("res.partner", string='Partner',readonly=True)
    external_id = fields.Char(string='External ID')