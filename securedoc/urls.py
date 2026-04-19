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
from django.conf import settings
from django.conf.urls.static import static
from portal import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.LoginPortalView.as_view(),name='login_view'),
    path('workspace/',views.StaffWorkspaceView.as_view(),name='workspace'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_view'),name='logout'),
    path('workspace/customers-list/',views.CustomersListView.as_view(),name='customers_list'),
    path('workspace/customers-list/<slug:customer_username>/profile/',views.CustomerProfileUpdateView.as_view(),name='customer_profile_edit'),
    path('workspace/customers-list/<str:customer_username>/profile/reset-password/',views.PasswordResetView.as_view(),name='admin_password_reset'),
    path('workspace/customers-list/<str:customer_username>/profile/delete-customer/',views.customer_delete,name='delete_customer'),
    path('workspace/customers-list/add-new-user/',views.CustomerCreationView.as_view(),name='add_customer'),
    path('workspace/add-new-request/',views.NewRequestView.as_view(),name='new_request'),
    path('workspace/<str:customer_username>/requests-hub/',views.CustomerRequestsHub.as_view(),name='customer_requests_hub'),
    path('workspace/<str:customer_username>/requests-hub/<int:request_id>/edit',views.EditRequestView.as_view(),name='customer_request_edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
