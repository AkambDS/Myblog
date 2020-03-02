from django.apps import AppConfig


class MyUserauthConfig(AppConfig):
    name = 'my_userauth'

    def ready(self):
        import users.signals
