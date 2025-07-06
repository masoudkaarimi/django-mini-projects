from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load all fixture data into the database"

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        fixtures = [
            "account/fixtures/groups.json",
            "account/fixtures/users.json",
            "loan/fixtures/loans.json",
            "loan/fixtures/installments.json",
            "loan/fixtures/installment_payments.json",
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("Starting fixture loading process...\n"))

        for fixture_path in fixtures:
            full_path = BASE_DIR / fixture_path

            if not full_path.exists():
                self.stderr.write(self.style.ERROR(f"Fixture file not found: {full_path}"))
                continue

            try:
                self.stdout.write(self.style.NOTICE(f"\nLoading fixture: {fixture_path} ..."))
                call_command('loaddata', str(full_path))
                self.stdout.write(self.style.SUCCESS(f"Loaded {fixture_path}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to load {fixture_path}: {e}"))

        self.stdout.write(self.style.SUCCESS("\nAll fixtures loaded successfully."))
