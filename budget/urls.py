from django.urls import path
from .views import (limits_list_view, create_limits_view, find_limit_view, create_budget_view,  
                    LimitDeleteView, LimitUpdateView)


urlpatterns = [
    path('', limits_list_view, name='limits_list'),
    path('create_limits/', create_limits_view, name='create_limits'),
    path('find_limit/', find_limit_view, name="find_limit"),
    path('create_budget/', create_budget_view, name='create_budget'),
    path('limit_delete/<int:pk>/', LimitDeleteView.as_view(), name="limit_delete"),
    path('limit_update/<int:pk>/', LimitUpdateView.as_view(), name="limit_update"),
]
