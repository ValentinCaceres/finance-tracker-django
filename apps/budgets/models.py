from django.db import models
from django.contrib.auth.models import User
from apps.categories.models import Category
from apps.accounts.models import Account
from decimal import Decimal


class Budget(models.Model):
    """
    Límites de gasto mensuales por categoría.
    """
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='Budget limit amount'
    )

    period = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        default='monthly'
    )

    year = models.IntegerField()

    month = models.IntegerField(
        null=True,
        blank=True,
        help_text='Only for monthly budgets (1-12)'
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
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        ordering = ['-year', '-month']
        unique_together = ['user', 'category', 'year', 'month']
    
    def __str__(self):
        if self.month:
            return f"{self.category.name} - {self.year}/{self.month:02d} - {self.amount}"
        return f"{self.category.name} - {self.year} - {self.amount}"
    
    def get_spent_amount(self):
        """Calculate total spent in this budget period"""
        from apps.transactions.models import Transaction
        from datetime import date
        
        if self.period == 'monthly':
            transactions = Transaction.objects.filter(
                user=self.user,
                category=self.category,
                transaction_type='expense',
                transaction_date__year=self.year,
                transaction_date__month=self.month
            )
        else:  # yearly
            transactions = Transaction.objects.filter(
                user=self.user,
                category=self.category,
                transaction_type='expense',
                transaction_date__year=self.year
            )
        
        total = sum(t.amount for t in transactions)
        return Decimal(str(total))
    
    def get_percentage_used(self):
        """Returns percentage of budget used"""
        spent = self.get_spent_amount()
        if self.amount == 0:
            return 0
        return float((spent / self.amount) * 100)


class Goal(models.Model):
    """
    Metas de ahorro del usuario.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=200,
        help_text='e.g., Vacation 2026'
    )

    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00')
    )

    target_date = models.DateField(
        help_text='Date to achieve this goal'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'
        ordering = ['target_date', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.current_amount}/{self.target_amount}"
    
    def get_percentage_complete(self):
        """Returns percentage of goal completed"""
        if self.target_amount == 0:
            return 0
        return float((self.current_amount / self.target_amount) * 100)
    
    def is_complete(self):
        """Check if goal is reached"""
        return self.current_amount >= self.target_amount


class RecurringTransaction(models.Model):
    """
    Plantilla para transacciones recurrentes (suscripciones, salarios).
    """
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.CharField(
        max_length=255
    )

    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES
    )

    day_of_month = models.IntegerField(
        null=True,
        blank=True,
        help_text='For monthly: day of month (1-31)'
    )
    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
        help_text='Leave blank for no end'
    )

    is_active = models.BooleanField(
        default=True
    )

    last_generated = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Recurring Transaction'
        verbose_name_plural = 'Recurring Transactions'
        ordering = ['-is_active', 'description']
    
    def __str__(self):
        return f"{self.description} - {self.get_frequency_display()}"