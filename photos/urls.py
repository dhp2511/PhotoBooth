from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomSignupView
from photos.views import page_not_found

handler404 = page_not_found

urlpatterns = [
    path("", views.global_view, name="global"),
    path("login/", views.loginUser, name="login"),
    path('user/login/', views.loginUser, name='login'),
    path("logout/", views.logoutUser, name="logout"),
    path("gallery/", views.gallery, name="gallery"),
    path("edit/<str:pk>", views.editPage, name="edit"),
    path(
        "delete_category/<int:category_id>/",
        views.delete_category_and_images,
        name="delete_category",
    ),
    path("like_photo/<str:pk>", views.like_photo, name="like_photo"),
    path("comment_photo/<str:pk>", views.comment_photo, name="comment_photo"),
    path("register/", views.registerUser, name="register"),
    path("photo/<str:pk>", views.viewPhoto, name="photo"),
    path("add/", views.addPhoto, name="add"),
    path("gallery/delete_images/", views.delete_images, name="delete_images"),
    path("delete_comment/<str:pk>", views.delete_comment, name="delete_comment"), 
    path('accounts/social/signup/', CustomSignupView.as_view(), name='socialaccount_signup'),
    path('/', include('verify_email.urls')),

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)