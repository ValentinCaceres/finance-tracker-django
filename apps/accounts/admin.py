from django.contrib import admin

# Register your models here.
from .models import Account

# Clase que PERSONALIZA cómo se administra Account
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_type', 'currency', 'current_balance', 'is_active', 'user']
    list_filter = ['account_type', 'currency', 'is_active', 'created_at']
    search_fields = ['name', 'user__username']

# Registrar CON la personalización
admin.site.register(Account, AccountAdmin)