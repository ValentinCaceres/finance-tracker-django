from django.contrib import admin

# Register your models here.
from .models import Budget
from .models import Goal

# Clase que PERSONALIZA cómo se administra Budget
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'period', 'year', 'month', 'is_active', 'created_at']
    list_filter = ['period', 'is_active', 'year', 'month', 'created_at']
    search_fields = ['user__username', 'category__name']
    ordering = ['-year', '-month', 'category__name']

# Registrar CON la personalización
admin.site.register(Budget, BudgetAdmin)

# Clase que PERSONALIZA cómo se administra Goal
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'target_amount', 'current_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'user__username']
    ordering = ['-created_at', 'name']

# Registrar CON la personalización
admin.site.register(Goal, GoalAdmin)