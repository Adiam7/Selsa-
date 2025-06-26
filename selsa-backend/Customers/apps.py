from django.apps import AppConfig

class OrderConfig(AppConfig):
    name = 'Customers'

    def ready(self):
        import Customers.signals
