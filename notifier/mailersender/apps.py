from django.apps import AppConfig
from mailersender.client import MailerSendClient
import os


class MailerSenderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailersender"

    def ready(self):
        """
        Initialize global services when the app is ready.
        """
        from mailersender import services

        services.mailersend_client = MailerSendClient(
            os.environ.get("MAILERSEND_EMAIL"),
            os.environ.get("MAILERSEND_NAME"),
            os.environ.get("MAILERSEND_API_KEY"),
        )