from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RatingConfig(AppConfig):
    name = 'rating'
    verbose_name = _('profiles')

    def ready(self):
        import rating.signals
