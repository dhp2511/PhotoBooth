from django.db import models

from django.core.validators import FileExtensionValidator

from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    image = models.ImageField(upload_to='images/',
        null=False,
        blank=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "bmp",
                    "webp",
                    "svg",
                    "tiff",
                    "tif",
                    "gif",
                    "heif",
                ]
            )
        ],
    )
    publicAccess = models.BooleanField(default=False, null=False, blank=False)
    description = models.TextField()
    upload_datetime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through="Like", related_name="liked_photos")
    comments = models.ManyToManyField(
        User, through="Comment", related_name="commented_photos"
    )

    def __str__(self):
        return self.description

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comment.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.photo}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.photo}"
