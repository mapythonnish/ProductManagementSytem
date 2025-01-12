from django.contrib import admin
from .models import User, Product, ProductColor

# Register the custom User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('username',)

admin.site.register(User, UserAdmin)

# Register the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price', 'published', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('published', 'created_by')
    ordering = ('created_at',)

admin.site.register(Product, ProductAdmin)

# Register the ProductColor model
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'sizes')
    search_fields = ('product__name', 'color')
    list_filter = ('color', 'sizes')
    ordering = ('product',)

admin.site.register(ProductColor, ProductColorAdmin)
