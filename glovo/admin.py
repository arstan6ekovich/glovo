from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Courier)
admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Review)
admin.site.register(Payment)