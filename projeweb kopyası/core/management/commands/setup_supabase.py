from django.core.management.base import BaseCommand
from config.supabase_setup import setup_database

class Command(BaseCommand):
    help = 'Sets up Supabase database tables'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Supabase database...')
        setup_database()
        self.stdout.write(self.style.SUCCESS('Successfully set up Supabase database')) 