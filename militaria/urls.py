from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'militaria'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('register/', views.registerView, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add/', views.AddWarehouse, name="new"),
    path('supply/', views.Supply, name='supply'),
    path('contact/', views.contactView, name="contact")
    ]