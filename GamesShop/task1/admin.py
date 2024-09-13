from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Buyer)
# admin.site.register(Game)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cost', 'age_limited')
    # fields = [
    #     ('title', 'age_limited'),
    #     'description',
    #     ('cost', 'size'),
    #     'buyer'
    # ]
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
