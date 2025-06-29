from celery import shared_task

from apps.checkout.services import CartService


@shared_task()
def clear_expired_reservations():
    CartService.clear_expired_reservations()

