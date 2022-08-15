from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.profiles'
    
    def ready(self): # Let our app knows about the signal which we created.
        from apps.profiles import signals