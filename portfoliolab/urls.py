"""portfoliolab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from project import views
from project.views import AddDonation, FormConfirmation, LandingPage, Login, Register, Logout, UserProfile, \
                          UserSettings, UserChangePw, RemindPassword, SetNewPass

urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),
    path('', LandingPage.as_view(), name='landing_page'),
    path('form/', AddDonation.as_view(), name='donation'),
    path('form_conf/', FormConfirmation.as_view(), name='confirmation'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('user_profile/', UserProfile.as_view(), name='profile'),
    path('settings', UserSettings.as_view(), name='settings'),
    path('settings/change-password', UserChangePw.as_view(), name="change-pw"),
    path('create/', views.create, name='create'),
    path('contact/', views.contact, name='email'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name="activate"),
    path('remind_password/', RemindPassword.as_view(), name="remind_pw"),
    path('remind_password_confirm/<uidb64>/<token>/', views.password_reset_confirm, name="pw_confirm"),
    path('new_password/', SetNewPass.as_view(), name="new_pw")
]
