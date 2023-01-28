from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, login_view, OrderListCreateView, OrderRetrieveUpdateDestroyView, get_emails, order_list

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('get-emails',get_emails,name='get_emails'),
    path('get-orders',order_list,name='order_list'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-retrieve-update-destroy'),
]
