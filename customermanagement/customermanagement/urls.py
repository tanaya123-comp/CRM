"""customermanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import  views as auth_views
from accounts.views import customer,products,dashboard,orderform,updateform,deleteorder,createcustomer,updatecustomer,deletecustomer,orderspecific, loginpage,registerPage,logoutuser,userPage,accounts_settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/<str:pk>/',customer,name="customer"),
    path('products/',products,name="products"),
    path('dashboard',dashboard,name="dashboard"),
    path('orderform',orderform,name="orderform"),
    path('updateform/<str:pk>/',updateform,name="updateform"),
    path('deleteorder/<str:pk>/',deleteorder,name="deleteorder"),
    path('createcustomer',createcustomer,name="createcustomer"),
    path('updatecustomer/<str:pk>/',updatecustomer,name="updatecustomer"),
    path('deletecustomer/<str:pk>/',deletecustomer,name="deletecustomer"),
    path('orderspecific/<str:pk>/',orderspecific,name="orderspecific"),
    path('login/',loginpage,name="login"),
    path('logoutuser/', logoutuser, name="logout"),
    path('registerpage',registerPage,name="register"),
    path('userpage',userPage,name='userpage'),
    path('account',accounts_settings,name='account_setting'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
