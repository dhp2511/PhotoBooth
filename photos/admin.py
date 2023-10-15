from django.contrib import admin

# Register your models here.

from .models import Photo, Category ,Like,Comment

admin.site.register(Photo)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)