from django.apps import AppConfig


class CategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Or 'UUIDField' if you use UUIDs project-wide
    name = 'category'
    verbose_name = 'Product Categories'
    label = 'category'  # Optional: can be used to refer to the app in migrations or other places
    icon = 'category'  # Optional: if you use a custom icon for the admin interface
    
    def ready(self):
        import category.signals
