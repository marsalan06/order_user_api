from django.contrib import admin
from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','item', 'customer', 'created_at')
    list_filter = ('customer', 'created_at')
    search_fields = ('customer__username', 'id')

admin.site.register(Order, OrderAdmin)