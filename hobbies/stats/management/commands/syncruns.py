from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Syncs running data'

    def add_arguments(self, parser):
        #parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        print("Running command ☄️")