from django.db import models
from products.models import Product, ProductVariant


class Urls(models.Model):
    """ Store URL's for course content """

    class Meta:
        """ Adjust plural of model name in admin """
        verbose_name_plural = 'URLs'

    course = models.ForeignKey(
        'CourseInfo',
        on_delete=models.CASCADE,
        related_name='course_week'
        )
    class_no = models.IntegerField(default=0)
    url = models.URLField()

    def __str__(self):
        return "Week " + str(self.class_no)

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
