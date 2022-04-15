from django.contrib import admin
from .models import CourseInfo, Urls


class UrlsAdminInline(admin.TabularInline):
    """ Set OrderLineItem admin to be visible from Order Admin """

    model = Urls
    fields = (
        'course', 'class_no',
        'url',
        )


class CourseInfoAdmin(admin.ModelAdmin):
    """ Admin settings for Order model """

    inlines = (UrlsAdminInline,)

    fields = ('course', 'variant',)

admin.site.register(CourseInfo, CourseInfoAdmin)
