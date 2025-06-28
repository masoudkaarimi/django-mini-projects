from apps.checkout.services import CartService


# from celery import shared_task

# @shared_task()
def clear_expired_reservations():
    CartService.clear_expired_reservations()

# admin.py:
# def save_model(self, request, obj, form, change):
#     super().save_model(request, obj, form, change)
#     promotion_prices.delay(obj.promo_reduction, obj.id)
#     promotion_management.delay()


# settings/base.py:
# CELERY_BROKER_URL = 'redis://redis:6379'
# CELERY_RESULT_BACKEND = 'redis://redis:6379'
#
# from celery.schedules import crontab
# CELERY_BEAT_SCHEDULE = {
#     'clear-expired-reservations': {
#         'task': 'tasks.clear_expired_reservations',
#         'schedule': crontab(minute=0, hour=0),
#     }
# }
