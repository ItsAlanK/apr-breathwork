from django.contrib import admin
from .models import AboutUs


class AboutUsAdmin(admin.ModelAdmin):
    """ Limit about us model to only one item to be edited """
    def has_add_permission(self, request):
        count = AboutUs.objects.all().count()
        if count == 0:
            return True
        return False

admin.site.register(AboutUs, AboutUsAdmin)
