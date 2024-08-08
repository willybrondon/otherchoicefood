from django.contrib import admin

from marketplace.models import Card

class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'created_at')
# Register your models here.
admin.site.register(Card, CardAdmin)
