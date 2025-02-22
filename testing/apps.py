from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class TestingConfig(AppConfig):
    name = 'testing'
    verbose_name = _('Testing')

    def ready(self):
        import testing.signals