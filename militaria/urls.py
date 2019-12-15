from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.conf.urls import url, include
from .serializers import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'warehouses', WarehouseViewSet)

# app_name = 'militaria'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('register/', views.registerView, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add/', views.AddWarehouse, name="new"),
    path('supply/', views.Supply, name='supply'),
    path('contact/', views.contactView, name="contact"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]




