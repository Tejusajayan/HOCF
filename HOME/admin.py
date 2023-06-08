from django.contrib import admin
from .models import *
# Register your models here.
class cartsearch(admin.ModelAdmin):
    search_fields=['orderid']

class finalsearch(admin.ModelAdmin):
    search_fields=['complete']

admin.site.register(food)
admin.site.register(review)
admin.site.register(customer)
admin.site.register(order)
admin.site.register(cartitem,cartsearch)
admin.site.register(finalord,finalsearch)
admin.site.register(dinereq)