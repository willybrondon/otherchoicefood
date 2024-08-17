from django.contrib import admin

from marketplace.models import Card, Tax

class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'created_at')
# Register your models here.
    
class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')

admin.site.register(Card, CardAdmin)
admin.site.register(Tax, TaxAdmin)
