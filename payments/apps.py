from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'

    def ready(self):
        import payments.signals
