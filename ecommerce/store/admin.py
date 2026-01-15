from django.contrib import admin
from .models import Category, Product, CartItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_preview')

    def icon_preview(self, obj):
        if obj.icon:
            return f'<img src="{obj.icon.url}" width="40" />'
        return "No Icon"
    icon_preview.allow_tags = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name',)


admin.site.register(CartItem)
admin.site.register(Order)
