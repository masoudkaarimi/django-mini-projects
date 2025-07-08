import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load all fixture data into the database"

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

        # Copy static images to media folder
        static_images = [
            'assets/images/placeholders/avatar.webp',
            'assets/images/placeholders/cover-photo.webp',
            # 'assets/images/placeholders/tag-thumbnail.webp',
            'assets/images/placeholders/category-thumbnail.webp',
            'assets/images/placeholders/post-thumbnail.webp',
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("Copying static images to media folder...\n"))

        for image_path in static_images:
            # Source path in static folder
            src = None
            for static_dir in settings.STATICFILES_DIRS:
                potential_src = os.path.join(static_dir, image_path)
                if os.path.exists(potential_src):
                    src = potential_src
                    break

            if not src:
                self.stderr.write(self.style.ERROR(f"Static image not found: {image_path}"))
                continue

            # Destination path in media folder
            filename = os.path.basename(image_path)
            dst = os.path.join(settings.MEDIA_ROOT, 'placeholders', filename)

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(dst), exist_ok=True)

            try:
                shutil.copy2(src, dst)
                self.stdout.write(self.style.SUCCESS(f"Copied {image_path} to {dst}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to copy {image_path}: {e}"))

        # Load fixtures
        fixtures = [
            "account/fixtures/groups.json",
            "account/fixtures/users.json",
            "account/fixtures/profiles.json",
            "blog/fixtures/tags.json",
            "blog/fixtures/categories.json",
            "blog/fixtures/posts.json",
            "blog/fixtures/comments.json",
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("\nStarting fixture loading process...\n"))

        for fixture_path in fixtures:
            full_path = BASE_DIR / fixture_path

            if not full_path.exists():
                self.stderr.write(self.style.ERROR(f"Fixture file not found: {full_path}"))
                continue

            try:
                self.stdout.write(self.style.NOTICE(f"\nLoading fixture: {fixture_path} ..."))
                call_command('loaddata', str(full_path))
                self.stdout.write(self.style.SUCCESS(f"✓ Loaded {fixture_path}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"✗ Failed to load {fixture_path}: {e}"))

        self.stdout.write(self.style.SUCCESS("\n🎉 All fixtures loaded successfully!"))
