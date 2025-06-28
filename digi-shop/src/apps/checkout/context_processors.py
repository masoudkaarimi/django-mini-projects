from apps.checkout.services import CartService


def cart(request):
    if request.user.is_authenticated:
        return {'cart': CartService.get_data(request.user)}
    return {'cart': None}
