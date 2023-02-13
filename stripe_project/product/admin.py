from django.contrib import admin

from product.models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Представление продуктов в админ-панели."""

    list_display = ('name', 'description', 'price', 'tax', 'currency')
    search_fields = ('name',)
    list_filter = ('currency', 'tax')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Представление заказов в админ-панели."""

    list_display = ('item',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Представление купоново в админ-панели."""

    list_display = ('id', 'percent_off')
    search_fields = ('id',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """Представление купоново в админ-панели."""

    list_display = ('display_name', 'inclusive', 'percentage')
    search_fields = ('display_name',)
    list_filter = ('inclusive',)
