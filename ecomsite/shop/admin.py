from django.contrib import admin
from .models import Order, OrderItem, ProductInfo, CartItem, Review ,Cart

admin.site.site_header = "E-Commerce Site Administration"
admin.site.site_title = "E-Commerce Site Admin Portal"
admin.site.index_title = "Welcome to the E-Commerce Site Admin Area"

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'availability', 'stock', 'created_at')
    search_fields = ('title', 'category', 'description')
    list_filter = ('category', 'availability', 'created_at')


admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Cart)
