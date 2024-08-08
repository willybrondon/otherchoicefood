from django.urls import path 
from . import views

urlpatterns = [
    path('', views.marketplace, name = 'marketplace'),
    
    path('<slug:vendor_slug>/', views.vendor_detail, name="vendor_detail"),
    # ADD to cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name="add_to_cart"),
    # descrese card 
    path('decrease_cart/<int:food_id>/', views.descrease_cart, name="decrease_cart"),
    # delete cart item
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart')
]
