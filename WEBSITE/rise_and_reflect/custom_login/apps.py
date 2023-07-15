from django.apps import AppConfig

class AppNameConfig(AppConfig):
    
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_login'
    # import your signal in the ready function
    def ready(self):
        import custom_login.signals