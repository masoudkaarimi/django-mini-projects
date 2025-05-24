import os

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load all fixtures in the correct order'

    def handle(self, *args, **kwargs):
        app_name = 'inventory'
        fixtures_dir = os.path.join('apps', app_name, 'fixtures')

        fixtures = [
            'brand',
            'category',
            'product_type',
            'product_attribute',
            'product_type_attribute',
            'product_attribute_value',
            'product',
            'product_inventory',
            'product_inventory_attribute_value',
            'stock',
            'media'
        ]

        self.stdout.write(self.style.NOTICE('Starting to load fixtures...'))

        # First, create directory if it doesn't exist
        os.makedirs(fixtures_dir, exist_ok=True)
        self.stdout.write(self.style.SUCCESS(f'Fixture directory: {os.path.abspath(fixtures_dir)}'))

        for fixture in fixtures:
            fixture_path = os.path.join(fixtures_dir, f'{fixture}.json')

            if not os.path.exists(fixture_path):
                self.stdout.write(self.style.WARNING(f'Fixture file not found: {fixture_path}'))
                continue

            self.stdout.write(self.style.NOTICE(f'Loading {fixture} fixture...'))
            try:
                call_command('loaddata', fixture_path)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to load {fixture}: {e}'))
                self.stdout.write(self.style.WARNING(
                    "Possible issues:\n"
                    "1. Have you run migrations? Try 'python manage.py migrate'\n"
                    "2. Check if model names in fixtures match your app configuration\n"
                    "3. Ensure the fixture JSON has 'model': 'inventory.ModelName'"
                ))
                return

        self.stdout.write(self.style.SUCCESS('All fixtures loaded successfully!'))
