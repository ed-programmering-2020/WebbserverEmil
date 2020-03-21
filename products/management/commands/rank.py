from django.core.management.base import BaseCommand
import inspect
import sys


class Command(BaseCommand):
    help = "Update the product rankings"

    def handle(self, *args, **kwargs):
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            print(obj)
            if inspect.isclass(obj):
                print("class")

                rank = getattr(self, "rank", None)
                if callable(rank):
                    obj.rank()
                    print("here")

        self.stdout.write(self.style.SUCCESS("Successfully updated all rankings"))
