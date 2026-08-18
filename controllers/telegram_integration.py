from odoo import http
from odoo.http import request,Request
import werkzeug
import json

class TelegramIntegration(http.Controller):

    def valid_response(self,data,status=200):
        return werkzeug.wrappers.Response(status=status,content_type='application/json',response=json.dumps(data))

    @http.route('/api/telegram/webhook',type='http',auth="public",methods=['POST'],csrf=False)
    def webhook(self,**kwargs):
        try:
            data = request.httprequest.data
            data = json.loads(data)
            print(f"Data : {data}")
            customer_account = request.env['customer.account.identity'].sudo()
            message = data.get('message')
            message_from = message.get('from')
            user_id = message_from.get('id')
            existing_user = customer_account.sudo().search([('external_id','=',user_id)])
            if existing_user:
                crm_lead = request.env['crm.lead'].sudo().search([('partner_id','=',existing_user.partner_id)])
                crm_lead.message_post(
                    body=message.get('text'),
                    message_type='comment'
                )
                return self.valid_response({
                    'success' : False,
                    'message' : "Customer Account Already Exists",
                })
            user_name = message_from.get('username')
            name = message_from.get('first_name')
            platform = 'Telegram'
            partner = request.env['res.partner'].sudo().create({
                'name': name,
                'social_platform': platform,
            })
            account = customer_account.create({
                'user_name' : user_name,
                'first_name' : name,
                'external_id' : user_id,
                'platform' : platform,
                'partner_id' : partner.id,
            })
            crm_lead = request.env['crm.lead'].sudo().create({
                'partner_id' : partner.id,
                "description" : "This Customer is come From Telegram",
            })
            crm_lead.message_post(
                body=message.get('text'),
                message_type='comment'
            )
            return self.valid_response({
                'success' : True,
                'message' : 'New Customer Account Created',
                'id' : account.id,
            })
        except Exception as e:
            return {
                'status' : 'fail',
                'message' : str(e)
            }