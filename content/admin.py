from django.contrib import admin
from .models import Product, Bid


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'bidder_name', 'bidder_email', 'bid_price', 'bidded_at', 'bidder_phone',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'product_name', 'product_size', 'current_price', 'buy_now', 'frame', 'sold',)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
