from mailersend import emails

from mailersender.metaclasses import MailerSendMeta


class MailerSendClient(metaclass=MailerSendMeta):
    def __init__(self, email_from: str = None, email_name: str = None, api_key: str = None):
        self.api_key = api_key
        self.email_from = email_from
        self.email_name = email_name
        self.client = emails.NewEmail(api_key)

    def send_email(self, recipient: str, template_id: str, variables: dict):
        try:
            self.client.send(
                {
                    'from': {'email': self.email_from, 'name': self.email_name},
                    'to': [{'email': recipient}],
                    "subject": "Hello from Events Notifier",
                    'template_id': template_id,
                    'personalization': [
                        {
                            'email': recipient,
                            'data': variables,
                        }
                    ]
                }
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")
