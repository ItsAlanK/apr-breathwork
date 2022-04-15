from django.db import models
from products.models import Product, ProductVariant
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Urls(models.Model):
    """ Store URL's for course content """

    class Meta:
        """ Adjust plural of model name in admin """
        verbose_name_plural = 'URLs'

    course = models.ForeignKey('CourseInfo', on_delete=models.CASCADE)
    class_no = models.IntegerField()
    url = models.URLField()


class CourseInfo(models.Model):
    """ Model for course info """

    class Meta:
        """ Adjust plural of model name in admin """
        verbose_name_plural = 'Course Info'

    course = models.OneToOneField(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    def __str__(self):
        date = self.variant.date.strftime('%B %d, %Y')
        return self.course.name + " " + date

@receiver(pre_save, sender=Product)
def my_handler(sender, **kwargs):
    if sender.pk is None:  # create
        sender.model = CourseInfo.objects.create(
            course = sender,
            variant = ProductVariant.objects.get(product=sender)
        )
