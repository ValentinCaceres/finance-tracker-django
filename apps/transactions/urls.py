from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path(
        '',
        views.TransactionListView.as_view(),
        name='list'
    ),
]