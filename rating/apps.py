from django.apps import AppConfig


class RatingConfig(AppConfig):
    name = 'rating'

    def ready(self):
        import rating.signals
