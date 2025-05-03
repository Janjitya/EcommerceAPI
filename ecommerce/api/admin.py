from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Category, CustomUser, Cart, CartItems, Review, ProductRating, Wishlist

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'price', 'featured', 'description', 'category' ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'slug']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register([CartItems, Review, ProductRating, Wishlist])

