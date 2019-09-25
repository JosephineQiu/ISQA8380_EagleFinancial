from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'portfolio'
urlpatterns = [

    path('', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customer/create/', views.customer_create, name='customer_create'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_new, name='stock_new'),
    path('stock/<int:pk>/edit', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete', views.stock_delete, name='stock_delete'),
    path('login/', views.user_login, name='login'),
    #path('login/',auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logout, name='logout'),
# reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# change password urls
    path('password_change/',auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

# Investments
    path('investment_list/', views.investment_list, name='investment_list'),
    path('investmenet_create/', views.investment_create, name='investment_create'),
    path('investment/<int:pk>/delete', views.investment_delete, name='investment_delete'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
]
