import datetime

from django.db import models
from django.utils import timezone

from accounts.models import Person

# Coupon Class Specifier
class Coupon(models.Model):
    owner = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        editable=False)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    terms = models.TextField()
    claimants = models.ManyToManyField(Person, through='Claim',
                                       related_name='Claimed')

    create_date = models.DateTimeField(
        default=timezone.now, editable=False)
    # When the coupon becomes ready for use
    publish_date = models.DateTimeField(
        default=timezone.now)
    # When this coupon expires
    validity = models.DateTimeField(
        default=timezone.now)
    '''
    # Use this method when we get to postgres
    validity = models.DurationField(
        default=datetime.timedelta(days=7), help_text="1 12:00 = 1 day + 12 hours")'''

    # Method to determine if coupon is currently published or not
    def published(self):
        return self.publish_date <= timezone.now() <= self.validity
    published.admin_order_field = 'publish_date'
    published.boolean = True
    published.short_description = 'Currently Running'

    # Human-readable name for Coupon
    def __str__(self):
        return self.title

# Relationship between Coupon and User
class Claim(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_claimed = models.DateTimeField(
        default=timezone.now, editable=False)
