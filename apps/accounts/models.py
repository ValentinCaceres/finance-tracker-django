from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Account(models.Model):
    """
    Cuentas financieras del usuario (banco, efectivo, tarjetas).
    """
    ACCOUNT_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank Account'),
        ('credit_card', 'Credit Card'),
        ('savings', 'Savings Account'),
        ('investment', 'Investment Account'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('CLP', 'Chilean Peso'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100,
        help_text='e.g., Banco Chile, Cash Wallet'
    )
    
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES
    )
    
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='CLP'
    )

    initial_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Starting balance when account was created'
    )

    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Current balance (calculated from transactions)'
    )

    is_active = models.BooleanField(
        default=True
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
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-is_active', 'name']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"
    
    def update_balance(self):
        """Recalculate balance from all transactions"""
        from apps.transactions.models import Transaction
        
        transactions = Transaction.objects.filter(account=self)
        balance = self.initial_balance
        
        for transaction in transactions:
            if transaction.transaction_type == 'income':
                balance += transaction.amount
            elif transaction.transaction_type == 'expense':
                balance -= transaction.amount
        
        self.current_balance = balance
        self.save()