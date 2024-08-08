from django.shortcuts import render, get_object_or_404
from marketplace.context_processors import get_cart_amounts, get_cart_counter
from marketplace.models import Card
from menu.models import Category, FoodItem
from django.http import HttpResponse, JsonResponse
from django.db.models import Prefetch
from vendor.models import Vendor
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors
    }
    return render(request, 'marketplace/listing.html', context)
def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'food_items',queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated():
        cart_items = Card.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vedor' : vendor,
        "categories" : categories,
        'cart_items' : cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try :
                fooditem = FoodItem.objects.get(food_id=food_id)
                # check if the user have user have aded tha food to the cart
                try :
                    checkcart = Card.objects.get(user=request.user, fooditem=fooditem)
                    # increase the cart quantity to the
                    checkcart.quantity +=1
                    checkcart.save()
                    
                    return JsonResponse({'status':'success', 'message':'Increase the cart quantity', 'cart_counter':get_cart_counter(request), 'qty':checkcart.quantity, 'cart_amount':get_cart_amounts(request)})
                except:
                    checkcart = Card.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    
                    return JsonResponse({'status':'Failed', 'message':'Added the food to the cart', 'qty': checkcart.quantity, 'cart_counter':get_cart_counter(request), 'cart_amount':get_cart_amounts(request)})

            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})
        else :
            return JsonResponse({'status':'Failed', 'message':'Invalide request'})
    
    else :
        
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})
    


def descrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try :
                fooditem = FoodItem.objects.get(food_id=food_id)
                # check if the user have user have aded tha food to the cart
                try :
                    checkcart = Card.objects.get(user=request.user, fooditem=fooditem)
                    if checkcart.quantity >1 :
                    # decrease the cart quantity to the
                        checkcart.quantity -=1
                        checkcart.save()
                    else : 
                        checkcart.delete()
                        checkcart.quantity = 0
                    
                    return JsonResponse({'status':'success', 'message':'Increase the cart quantity', 'cart_counter':get_cart_counter(request), 'qty':checkcart.quantity, 'cart_amount':get_cart_amounts(request)})
                except:
                    checkcart = Card.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    
                    return JsonResponse({'status':'Failed', 'message':'Added the food to the cart', 'qty': checkcart.quantity})

            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})
        else :
            return JsonResponse({'status':'Failed', 'message':'Invalide request'})
    
    else :
        
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})

@login_required(login_url ='login')    
def cart(request):
    cart_items = Card.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items' : cart_items
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated():
        if request.is_ajax():
            try :
                # check if the cart item exist
                cart_item = Card.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                return JsonResponse({'status':'success', 'message':'cart item has been deleted', 'cart_counter':get_cart_counter(request), 'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'cart item does not exist'})

        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})