from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """ Admin settings for Order model """

    readonly_fields = ('paid_member_from', 'is_paid_member',)

    fields = (
        'paid_member_from', 'is_paid_member',
        )

admin.site.register(UserProfile)
