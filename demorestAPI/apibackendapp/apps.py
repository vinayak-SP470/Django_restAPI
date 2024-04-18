from django.apps import AppConfig
class ApibackendappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apibackendapp'
    def ready(self):

        import apibackendapp.signals


