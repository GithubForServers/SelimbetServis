from django.contrib import admin
from .models import Category, Subcategory, Product,User

admin.site.register(Category)
admin.site.register(Subcategory)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username', 'user_id']  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price', 'created_at')
    list_filter = ('category', 'subcategory', 'created_at')
    search_fields = ('name', 'description')
    list_per_page = 20

