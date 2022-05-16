import datetime
from ckeditor.fields import RichTextField
from django.db import models


class Category(models.Model):
    """ Model for product categories """
    class Meta:
        """ Adjust plural of model name in admin """
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """ Returns category friendly name """
        return self.friendly_name


class Product(models.Model):
    """ Model for base products """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = RichTextField()
    duration = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    account_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """ Model for product variants (different time/dates) """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=datetime.time(13, 00))
    attendance_limit = models.IntegerField(default=100)
    places_sold = models.IntegerField(editable=False, default=0)
    meeting_invite_link = models.URLField(
        max_length=1024, null=True, blank=True)

    def __str__(self):
        product = self.product.name
        date = self.date.strftime('%B %d, %Y')
        time = self.time.strftime('%H:%M')
        return product + " " + date + " " + time
