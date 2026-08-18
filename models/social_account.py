from odoo import api, fields, models
from odoo.exceptions import ValidationError
import requests

class SocialAccount(models.Model):
    _name = "social.acc"
    _description = "Social Account"

    name = fields.Char(required=True)
    access_token = fields.Char(string="Access Token",required=True)
    bot_name = fields.Char(string="Bot Name",readonly=True)
    platform = fields.Selection([('telegram','Telegram')], string="Platform")
    account_id = fields.Char(string="Account ID",readonly=True)

    def sync_account(self):
        self.ensure_one()
        print(self.access_token)
        response = requests.get("https://api.telegram.org/bot" + self.access_token + "/getMe")
        if not response:
            raise ValidationError("Invalid Token")
        data = response.json()
        result = data['result']
        self.account_id = result["id"]
        self.bot_name = result["username"]


    def action_connect(self):
        self.ensure_one()
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        https_url = f"https{web_base_url[4:]}"
        print(https_url)
        url = https_url + "/api/telegram/webhook"
        telegram_url = (
            f"https://api.telegram.org/bot"
            f"{self.access_token}/setWebhook"
        )
        response = requests.post(telegram_url,params={'url':url},timeout=10)
        print(f"Status : {response.status_code}")
        print(f"Error : {response.text}")
        response.raise_for_status()
        return True


    @api.model
    def create(self, values):
        record = super(SocialAccount,self).create(values)
        record.sync_account()
        return record

