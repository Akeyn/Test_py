from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    name = 'Test_py.apps.registration'
    verbose_name = "Registration"

    def ready(self):
        import Test_py.apps.registration.signals.handlers