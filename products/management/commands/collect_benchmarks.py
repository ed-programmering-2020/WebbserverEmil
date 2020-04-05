from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Update specification rankings"

    def handle(self, *args, **kwargs):
        for content_type in ContentType.objects.all():
            model_class = content_type.model_class()

            rank = getattr(model_class, "rank", None)
            if callable(rank):
                model_class.rank()

        self.stdout.write(self.style.SUCCESS("Successfully updated all rankings"))
