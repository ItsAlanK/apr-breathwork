import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paid_member_from = models.DateField(default=datetime.date.today)
    is_paid_member = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()


@receiver(user_logged_in)
def check_is_paid_status(sender, user, request, **kwargs):
    """
    When user logs in confirms their is_paid_member status.
    Checks against current date to see whether time is still left
    on membership. Resets status is time expired.
    """
    user_profile = request.user.userprofile
    if user_profile.is_paid_member:
        current_date = datetime.date.today()
        difference = (current_date - user_profile.paid_member_from).days
        if difference > 42:
            user_profile.is_paid_member = False
            user_profile.save()
            print('Expired')
