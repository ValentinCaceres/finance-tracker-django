from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Categorías para clasificar transacciones.
    Pueden ser jerárquicas (padre-hijo).
    """
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    COLOR_CHOICES = [
        ('#EF4444', 'Red'),
        ('#F59E0B', 'Orange'),
        ('#10B981', 'Green'),
        ('#3B82F6', 'Blue'),
        ('#8B5CF6', 'Purple'),
        ('#EC4899', 'Pink'),
        ('#6B7280', 'Gray'),
    ]
    
    name = models.CharField(
        max_length=100
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        default='expense'
    )

    color = models.CharField(
        max_length=7,
        choices=COLOR_CHOICES,
        default='#3B82F6',
        help_text='Color for charts and UI'
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Icon name (e.g., lucide icon name)'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        help_text='Parent category for hierarchical structure'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='Leave blank for default categories'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['transaction_type', 'name']
        unique_together = ['name', 'user', 'transaction_type']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def get_full_path(self):
        """Returns full category path: Parent > Child"""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name