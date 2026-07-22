import firebase_admin
from firebase_admin import credentials, messaging
from core.env import settings

class FirebaseClient:
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized and getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None):
            try:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                cls._initialized = True
                print("Firebase Admin SDK inicializado exitosamente.")
            except Exception as e:
                print(f"Error inicializando Firebase: {e}")

    @staticmethod
    def send_notification(token: str, title: str, body: str, data: dict = None) -> bool:
        if not FirebaseClient._initialized:
            print("Firebase no está inicializado, no se envió la notificación.")
            return False
            
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data if data else {},
                token=token
            )
            response = messaging.send(message)
            print(f"Notificación enviada exitosamente a {token}: {response}")
            return True
        except Exception as e:
            print(f"Error enviando notificación a {token}: {e}")
            return False

firebase_client = FirebaseClient()
