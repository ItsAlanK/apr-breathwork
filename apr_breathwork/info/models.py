from ckeditor.fields import RichTextField
from django.db import models


class AboutUs(models.Model):
    """ Store About us content to be easily editable """

    class Meta:
        """ Adjust plural of model name in admin """
        verbose_name_plural = 'About Us'

    content = RichTextField(default="About us details")
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return 'About Us'
