import firebase_admin
from firebase_admin import credentials, messaging
from app.core.config import settings
import logging

class NotificationService:
    def __init__(self):
        try:
            # Check if Firebase is configured
            if settings.FIREBASE_CREDENTIALS_PATH:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                self.enabled = True
            else:
                self.enabled = False
        except Exception as e:
            logging.error(f"Firebase initialization failed: {e}")
            self.enabled = False

    async def send_push_notification(self, token: str, title: str, body: str, data: dict = None):
        if not self.enabled:
            logging.info(f"FCM disabled. Notification to {token}: {title} - {body}")
            return

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            token=token,
        )
        try:
            response = messaging.send(message)
            return response
        except Exception as e:
            logging.error(f"Failed to send FCM: {e}")

notification_service = NotificationService()
