from django.contrib import admin

# Register your models here.
from .models import Transaction

# Clase que PERSONALIZA cómo se administra Transaction
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'transaction_type', 'category', 'amount', 'transaction_date', 'created_at']
    list_filter = ['transaction_type', 'category', 'transaction_date', 'created_at']
    search_fields = ['description', 'notes', 'account__name', 'category__name', 'user__username']
    ordering = ['-transaction_date','-created_at']

# Registrar CON la personalización
admin.site.register(Transaction, TransactionAdmin)