from .models import Card, cart

from menu.models import FoodItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated():
        try:
            cart_items = cart.objects.filter(user=request.user)
            if cart_items :
                for cart_item in cart_items :
                    cart_count += cart_item.quantity()
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count = cart_count)

def get_cart_amounts(request):
    subtotal =0 
    tax = 0
    grand_total =0
    if request.user.is_authenticated():
        cart_items = Card.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = fooditem.objects.get(pk=item.fooditem)
            subtotal += (fooditem.price * item.quantity) # it means that subtotal = subtotal + (fooditem.price * item.quantity)
        grand_total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)
