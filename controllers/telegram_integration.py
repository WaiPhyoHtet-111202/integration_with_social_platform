import json
import logging
import requests
import werkzeug
import base64
from odoo import http
from odoo.http import request
from markupsafe import Markup

_logger = logging.getLogger(__name__)

class TelegramIntegration(http.Controller):

    def valid_response(self,data,status=200):
        return werkzeug.wrappers.Response(status=status,content_type='application/json',response=json.dumps(data))

    def save_file(self,file_id,crm_lead):
        social_acc = request.env['social.acc'].sudo().search([('platform','=','telegram')], limit=1)
        access_token = social_acc.access_token
        _logger.info(access_token)
        response = requests.get(
            "https://api.telegram.org/bot" + access_token + "/getFile?file_id=" + file_id,
            timeout=10,
        )
        response = response.json()
        if not response['ok']:
            return self.valid_response({
                'success': False,
                'message' : "File Id is not specified"
            })
        result = response['result']
        file_path = result.get('file_path')
        download_url = f"https://api.telegram.org/file/bot{access_token}/{file_path}"
        file_reponse = requests.get(download_url, timeout=10)
        file_reponse.raise_for_status()
        file_content = file_reponse.content
        encode_string = base64.b64encode(file_content)
        attachment = request.env['ir.attachment'].sudo().create({
            'name': 'Telegram Photo',
            'type' : 'binary',
            'datas' : encode_string,
            'mimetype' : 'image/jpeg',
            'res_model' : crm_lead._name,
            'res_id' : crm_lead.id
        })
        return attachment

    @http.route('/api/telegram/webhook',type='http',auth="public",methods=['POST'],csrf=False)
    def webhook(self,**kwargs):
        try:
            payload = request.httprequest.data or b"{}"
            data = json.loads(payload)
            _logger.info(data)
            message = data.get('message')
            if not message:
                _logger.info("Telegram update ignored because it has no message payload: %s", data)
                return self.valid_response({
                    'success': True,
                    'message': 'Update ignored',
                })

            message_from = message.get('from') or {}
            user_id = message_from.get('id')
            if not user_id:
                return self.valid_response({
                    'success': False,
                    'message': 'Missing Telegram user id',
                }, status=400)

            customer_account = request.env['customer.account.identity'].sudo()
            existing_user = customer_account.search([('external_id','=',str(user_id))], limit=1)
            message_text = message.get('text') or ''
            photo = message.get('photo')
            if existing_user:
                crm_lead = request.env['crm.lead'].sudo().search(
                    [('partner_id', '=', existing_user.partner_id.id)],
                    limit=1,
                )
                if photo:
                    best_photo = photo[-1]
                    file_id = best_photo['file_id']
                    attachment = self.save_file(file_id,crm_lead)
                    _logger.info(crm_lead.id)
                    body = Markup(f"""
                    <p>Telegram Photo</p>
                   <img src="/web/image/{attachment.id}" style="max-width:500px ; max-height:500px;" />
                    """)
                    crm_lead.message_post(
                        body=body,
                        message_type='comment',
                        attachment_ids = [attachment.id]
                    )

                if crm_lead and message_text:
                    crm_lead.message_post(
                        body=message_text,
                        message_type='comment'
                    )
                return self.valid_response({
                    'success': True,
                    'message': 'Customer Account Already Exists',
                })

            user_name = message_from.get('username')
            first_name = message_from.get('first_name') or user_name or 'Telegram Customer'
            platform = 'Telegram'
            partner = request.env['res.partner'].sudo().create({
                'name': first_name,
                'email' : user_name or first_name,
                'social_platform': platform,
            })
            account = customer_account.create({
                'user_name': user_name,
                'first_name': first_name,
                'external_id': str(user_id),
                'platform': platform,
                'partner_id': partner.id,
            })
            crm_lead = request.env['crm.lead'].sudo().create({
                'name' : first_name or user_name or 'Telegram Customer',
                'partner_id': partner.id,
                "description": "This Customer is come From Telegram",
            })
            if message_text:
                crm_lead.message_post(
                    body=message_text,
                    message_type='comment'
                )
            return self.valid_response({
                'success': True,
                'message': 'New Customer Account Created',
                'id': account.id,
            })
        except json.JSONDecodeError:
            return self.valid_response({
                'success': False,
                'message': 'Invalid JSON payload',
            }, status=400)
        except Exception as e:
            _logger.exception("Telegram webhook failed")
            return self.valid_response({
                'success': False,
                'message': 'Internal server error',
            }, status=500)
