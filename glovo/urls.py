from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/users/', UserListView.as_view(), name='user-list'),

    path('restaurants/', RestaurantListCreateView.as_view()),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view()),
    path('menu-categories/', MenuCategoryListCreateView.as_view()),
    path('menu-items/', MenuItemListCreateView.as_view()),

    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('order-items/', OrderItemListView.as_view()),

    path('couriers/', CourierListCreateView.as_view()),

    path('addresses/', AddressListCreateView.as_view()),

    path('reviews/', ReviewListCreateView.as_view()),

    path('payments/', PaymentListCreateView.as_view()),
]
