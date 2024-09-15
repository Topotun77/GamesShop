from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Buyer)
# admin.site.register(Game)


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'age')
    fields = [
        'name',
        ('balance', 'age'),
    ]
    search_fields = ('name', 'balance', 'age')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cost', 'age_limited')
    fieldsets = (
        ('Description', {
            'fields': (('title', 'age_limited'),
                       'description',)
        }),
        ('Parameters', {
            'fields': (('cost', 'size'),
                       'buyer')
        })
    )
    search_fields = ('title', 'cost')
    list_filter = ('buyer', 'title', 'cost', 'age_limited', 'size')
