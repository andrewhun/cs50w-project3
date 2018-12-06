from django.contrib import admin
from .models import Pasta, Salad, Topping, Pizza, Platter, Sub, Cart, Order, Extra



# Register your models here.

admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Platter)
admin.site.register(Sub)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Extra)