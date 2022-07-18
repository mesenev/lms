from django.core.management import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Command(BaseCommand):
    help = 'Sends message to a specific channel'

    def add_arguments(self, parser):
        parser.add_argument('channel_name', type=str)
        parser.add_argument('message', type=str)

    def handle(self, *args, **options):
        channels = get_channel_layer()
        async_to_sync(channels.group_send)(
            options['channel_name'], {'type': 'chat_message', 'message': options['message']}
        )
        self.stdout.write(self.style.SUCCESS(
            f'Message sent to channel {options["channel_name"]}'
        ))
