from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    
    def ready(self):
        import orders.signals
