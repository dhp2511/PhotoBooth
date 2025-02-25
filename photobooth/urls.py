"""
URL configuration for photobooth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from allauth.socialaccount.providers.google.views import oauth2_login, oauth2_callback
from allauth.account.views import logout
from django.contrib.auth import views as auth_views
# from django.conf.urls import handler400


urlpatterns = [
    path("admin/", admin.site.urls), 
    path("", include("photos.urls")),
    path("user/", include("users.urls")), 
    path('verification/', include('verify_email.urls')),
    path('accounts/logout/', logout, name="account_logout"),
    path('accounts/google/login/', oauth2_login, name="google_login"),
    path('accounts/google/login/callback/', oauth2_callback, name="google_callback"), 
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_form.html'), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name="password_reset_complete"),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  