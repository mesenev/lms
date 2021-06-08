from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RatingConfig(AppConfig):
    name = 'rating'

    def ready(self):
        import rating.signals
