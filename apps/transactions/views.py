from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction

# Create your views here.
class TransactionListView(
    LoginRequiredMixin,
    ListView
):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-transaction_date']
    paginate_by = 20

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related(
            'category',
            'account',
            'destination_account'
        )
    