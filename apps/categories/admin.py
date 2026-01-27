from django.contrib import admin

# Register your models here.
from .models import Category

# Clase que PERSONALIZA cómo se administra Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'transaction_type', 'color', 'parent', 'is_active']
    list_filter = ['transaction_type', 'is_active', 'created_at']
    search_fields = ['name', 'icon', 'parent__name', 'user__username']


# Registrar CON la personalización
admin.site.register(Category, CategoryAdmin)