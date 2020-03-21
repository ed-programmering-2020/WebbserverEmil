from django.core.management.base import BaseCommand
import inspect
import sys


class Command(BaseCommand):
    help = "Update the product rankings"

    def handle(self, *args, **kwargs):
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):

                rank = getattr(self, "rank", None)
                if callable(rank):
                    obj.rank()

        self.stdout.write(self.style.SUCCESS("Successfully updated product rankings"))
