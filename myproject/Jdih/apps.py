from django.apps import AppConfig


class JdihConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Jdih'

    def ready(self):
        import Jdih.signals
