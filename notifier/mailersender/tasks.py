from celery import shared_task

from mailersender.services import mailersend_client
from config.logger import LOGGER


@shared_task
def send_email_task(recipient: str, template_id: str, variables: dict):
    """
    Celery task to send an email using MailerSendClient.
    """
    try:
        mailersend_client.send_email(recipient, template_id, variables)
    except Exception as e:
         LOGGER.exception(f"Failed to send email: {e}")
