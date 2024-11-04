from .cart import Cart

def cart_badge(request):
    cart = Cart(request)
    item_count = sum(item['cantidad'] for item in cart)
    return {'cart_badge': item_count}