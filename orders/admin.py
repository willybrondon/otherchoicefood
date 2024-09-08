from django.contrib import admin
from .models import Payment, Order, OrderedFood
# Register your models here.


class OrderedFoodInline(admin.TabularInline):
    models = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantiy', 'price','amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    models = ['order_number', 'name', 'phone', 'email', 'total', 'payme_method', 'status','order_placed_to', 'is_ordered']
    inlines = [OrderedFoodInline]

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderedFood)
