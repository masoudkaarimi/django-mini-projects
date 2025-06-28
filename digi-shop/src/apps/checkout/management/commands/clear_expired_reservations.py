from django.core.management.base import BaseCommand

from apps.checkout.services import CartService


class Command(BaseCommand):
    help = 'Clear expired cart item reservations'

    def handle(self, *args, **options):
        count = CartService.clear_expired_reservations()
        self.stdout.write(self.style.SUCCESS(f'Successfully cleared {count} expired reservations'))
