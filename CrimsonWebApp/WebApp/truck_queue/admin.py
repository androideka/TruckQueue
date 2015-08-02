from django.contrib import admin

# Register your models here.
from .models import *


class TruckAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['truck_name']}),
        ('Truck information',   {'fields': ['truck_description', 'truck_day']}),
    ]


admin.site.register(Truck, TruckAdmin)
admin.site.register(MenuItems)
admin.site.register(Employee)
