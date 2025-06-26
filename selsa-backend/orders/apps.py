from django.apps import AppConfig

class OrderConfig(AppConfig):
    name = 'orders'

    def ready(self):
        import orders.signals
