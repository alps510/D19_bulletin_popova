from django.apps import AppConfig


class PostAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post_app'

    def ready(self):
        import post_app.signals
        #import post_app.tasks
