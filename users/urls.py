from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from users.views import *

handler404 = 'users.views.page_not_found'

urlpatterns = [
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("<username>", views.view_profile, name="view_profile"),
    path("delete/", views.profile_delete, name="profile_delete"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)