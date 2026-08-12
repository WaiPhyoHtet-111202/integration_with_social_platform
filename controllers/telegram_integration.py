from odoo import http
from odoo.http import request

class TelegramIntegration(http.Controller):

    @http.route('/api/telegram/webhook',type='http',auth="none",methods=['POST'],csrf=False)
    def webhook(self,**kwargs):
        data = request.jsonrequest
        print(data)