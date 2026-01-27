from django.db import models
from django.contrib.auth.models import User
from apps.categories.models import Category
from apps.accounts.models import Account
from decimal import Decimal


class Transaction(models.Model):
    """
    Registro de ingresos, gastos y transferencias.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
        help_text='Source account'
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='Amount in account currency'
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    transaction_date = models.DateField(
        help_text='Date when transaction occurred'
    )
    
    # For transfers
    destination_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='incoming_transfers',
        help_text='Only for transfers'
    )
    
    # Attachments
    receipt = models.ImageField(
        upload_to='receipts/%Y/%m/',
        null=True,
        blank=True,
        help_text='Receipt or invoice image'
    )
    
    # Recurring transaction reference
    recurring_transaction = models.ForeignKey(
        'budgets.RecurringTransaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_transactions'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
            models.Index(fields=['account', 'transaction_date']),
        ]
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} - {self.transaction_date}"
    
    def save(self, *args, **kwargs):
        """Update account balance when transaction is saved"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update account balance
        if is_new:
            self.account.update_balance()
            if self.destination_account:
                self.destination_account.update_balance()