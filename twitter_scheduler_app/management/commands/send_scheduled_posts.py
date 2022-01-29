from django.core.management.base import BaseCommand, CommandError
from twitter_scheduler_app.models import Post

class Command(BaseCommand):
    help = 'Send scheduled posts on twitter'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Sending posts started"))
        Post.send_scheduled_posts()
        self.stdout.write(self.style.SUCCESS("Sending posts ended successfully"))
