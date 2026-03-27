"""
URL configuration for securedoc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portal import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.LoginPortalView.as_view(),name='login_view'),
    path('workspace/',views.workspace,name='workspace'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_view'),name='logout'),
    path('workspace/users/',views.CustomerListView.as_view(),name='users_view'),
    path('workspace/users/<str:customer_username>/profile/',views.CustomerProfileUpdateView.as_view(),name='users_profile'),
    path('workspace/users/<str:customer_username>/profile/reset-password/',views.PasswordResetView.as_view(),name='admin_password_reset'),
]
