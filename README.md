# integration_with_social_platform
This project is used for to integrate with social platform by using odoo
Integration With Telegram

1. Need Telegram Bot To Generate Token
2. Verify Token Use Browser Or Terminal => https://api.telegram.org/bot{My Token}/getMe
3. set up Odoo url with https => ssh -p 443 -R0:localhost:8069 free.pinggy.io
4. Need To Connect With My Api To Telegram => https://api.telegram.org/bot{My Token}/setWebhook?url={My Https Link With Api}
5. Need To Check Info With https://api.telegram.org/bot{My Token}/getWebhookInfo

To Save Image From Telegram

1.
Telegram update ထဲက file_id ကိုယူ
2.
Telegram API getFile နဲ့ file path ရယူ
3.
file/bot<TOKEN>/<file_path> URL ကနေ file download လုပ်
4.
Download လုပ်ထားတဲ့ bytes ကို base64 encode လုပ်
5.
ir.attachment create လုပ်
6.
အဲဒီ attachment ကို crm.lead.message_post() နဲ့ chatter ထဲချိတ်

photoကိုchatterမှာပေါ်ချင်ရင်bodyမှာHtml tagအနေနဲ့ထည့်ပေးရန်လို odooကhtmlဖြစ်ကြောင်းသိစေရန်Markupသုံးရန်လို 
eg => body = Markup(f"""<p>Photo</><img src="/web/image/attachment id">"")