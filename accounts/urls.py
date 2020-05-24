from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('user/', views.user_page, name="user-page"),
    path('products/', views.product, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'),
    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),
]
