from datetime import date
import datetime
from django.shortcuts import redirect , render, get_object_or_404
from accounts.models import UserProfile
from marketplace.context_processors import get_cart_amounts, get_cart_counter
from marketplace.models import Card
from menu.models import Category, FoodItem
from django.http import HttpResponse, JsonResponse
from django.db.models import Prefetch
from vendor.models import OpenHour, Vendor
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
#from django.contrib.gis.mesure import D # D is the shortcut of distance
#from django.contrib.gis.db.models.function import Distance
from order.forms import OrderForm
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors,
        'vendor_count' : vendor_count
    }
    return render(request, 'marketplace/listing.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'food_items',queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    opening_hours = OpenHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    # check the curret day opening hour 
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpenHour.objects.filter(vendor=vendor, day=today)
    
    if request.user.is_authenticated():
        cart_items = Card.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vedor' : vendor,
        "categories" : categories,
        'cart_items' : cart_items,
        'opening_hours' : opening_hours,
        'current_opening_hours': current_opening_hours,
        
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
        
def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else :


        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']
        # get vendor ids that has the food item the user is looking for
        fecth_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)

        vendors = Vendor.objects.filter(Q(id__in=fecth_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
        
        if latitude and longitude and radius :
            pnt = GEOSGeometry('POINT(% %)' % (longitude, latitude))
            vendors = Vendor.objects.filter(Q(id__in=fecth_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),user_profile__distance_Ite=(pnt, D(km=2)))
            user_profile__distance_Ite = (pnt, D(km=radius)).annotate(distance=Distance('user_profile__location', pnt)).order_by('distance')
        
            for v in vendors :
                v.kms = round(v.distance.km)
        vendor_count = vendors.count()
        context= {
            'vendors' : vendors,
            'vendor_count' : vendor_count,
            'source_location': address,

        }

        return render(request, 'marketplace/listings.html', context)
    

@login_required(login_url='login')
def checkout(request):
    cart_items = Card.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'phone': user_profile.phone_number,
        'email' : user_profile.email,
        'address' : user_profile.address,
        'country' : user_profile.country,
        'state' : user_profile.state,
        'city' : user_profile.city,
        'pin_code' : user_profile.pin_code

    }
    form = OrderForm(initial= default_values)
    context = {
        'form' : form,
        'cart_items' : cart_items,
        'cart_count' : cart_count,
    }
    return render(request, 'marketplace/checkout.html', context)