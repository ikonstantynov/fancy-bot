import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    id = models.IntegerField(_('user id'), primary_key=True, editable=False)
    name = models.CharField(_('user name'), max_length=100)
    first_name = models.CharField(_('first name'), max_length=128)
    last_name = models.CharField(_('last name'), max_length=128, null=True, blank=True)
    username = models.CharField(_('user name'), max_length=128, null=True, blank=True)
    is_bot = models.BooleanField(_('is bot'))
    date_joined = models.DateTimeField(_('joined at'), default=timezone.now, blank=False, null=False)
    date_last_seen = models.DateTimeField(_('last seen at'), default=timezone.now, blank=False, null=False)


class Cryptocurrency(models.Model):
    short_name = models.CharField(_('currency short name'), max_length=10)
    full_name = models.CharField(_('currency full name'), max_length=100)
    currency_owner = models.CharField(_('currency owner name'), max_length=100)


class SubscriptionType(models.Model):
    class Subscriptions(models.TextChoices):
        MAX = 'MAX', _('Max')
        MIN = 'MIN', _('MIN')
        AVERAGE = 'AVG', _('Average')
    name = models.CharField(_('subscription name'), choices=Subscriptions.choices)


class SubscriptionStatusType(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
    status = models.CharField(_('subscription status'), choices=Status.choices)


class UserSubscription(models.Model):
    id = models.UUIDField(_('user subscription id'), primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency_id = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    subscription_type_id = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    subscription_status_id = models.ForeignKey(SubscriptionStatusType, on_delete=models.CASCADE)
    currency_rate = models.DecimalField(_('currency rate'))
    date_last_notified = models.DateTimeField(_('joined at'), blank=False, null=True)
    date_created = models.DateTimeField(_('created at'), default=timezone.now, blank=False, null=False)
