from django.urls import path
from .views import (BalanceUpdateView, TransactionUpdateView, TransactionDeleteView,
                    transaction_create_view, transactions_list, find_transaction_view,)

urlpatterns = [
    path('balance_update/', BalanceUpdateView.as_view(), name='balance_update'),
    path('', transactions_list, name='transactions_list'),
    path('create_transaction_set/', transaction_create_view, name='create_transaction_set'),
    path('find_transaction/', find_transaction_view, name="find_transaction"),
    path('transaction_update/<int:pk>/', TransactionUpdateView.as_view(), name="transaction_update"),
    path('transaction_delete/<int:pk>/', TransactionDeleteView.as_view(), name="transaction_delete"),
    
]
