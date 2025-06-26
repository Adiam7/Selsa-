from djangoql.schema import DjangoQLSchema

class ProductQLSchema(DjangoQLSchema):
    @property
    def model(self):
        from .models import Product
        return Product

class MyDjangoQLSchema(DjangoQLSchema):
    @property
    def exclude(self):
        from .models import Order
        return (Order,)

    def get_fields(self, model):
        from .models import Customer
        if model == Customer:
            return ['name']
        return super().get_fields(model)

class MyDjangoQLSchema(ProductQLSchema):
    @property
    def exclude(self):
        from .models import Order, OrderItem
        return (Order, OrderItem)

    def get_fields(self, model):
        from .models import Customer
        if model == Customer:
            return ['name', 'email', 'phone']
        return super().get_fields(model)