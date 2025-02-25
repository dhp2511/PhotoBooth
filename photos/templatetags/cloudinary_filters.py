from django import template
from cloudinary.utils import cloudinary_url

register = template.Library()

@register.filter(name='cloudinary_thumbnail')
def cloudinary_thumbnail(image_url):
    """Transforms Cloudinary image URL to a thumbnail with c_thumb, h_500, q_40, but skips GIFs."""
    if not image_url:
        return ""
    # Modify the Cloudinary URL for other images
    return image_url.replace("/upload/", "/upload/c_thumb,h_500,q_40/")
