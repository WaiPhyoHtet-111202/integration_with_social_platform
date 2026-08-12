# integration_with_social_platform
This project is used for to integrate with social platform by using odoo
Integration With Telegram

1. Need Telegram Bot To Generate Token
2. Verify Token Use Browser Or Terminal => https://api.telegram.org/bot{My Token}/getMe
3. set up Odoo url with https => ssh -p 443 -R0:localhost:8069 free.pinggy.io
4. Need To Connect With My Api To Telegram => https://api.telegram.org/bot{My Token}/setWebhook?url={My Https Link With Api}
5. Need To Check Info With https://api.telegram.org/bot{My Token}/getWebhookInfo

