from django.dispatch import Signal
from django.utils.deprecation import MiddlewareMixin

product_viewed = Signal()


class ProductViewTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.product_viewed_signal = product_viewed
