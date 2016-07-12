import datetime

from django.db import models
from django.utils import timezone

# Coupon Class Specifier
class Coupon(models.Model):
    # Creator of coupon
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, primary_key=True)
    terms = models.TextField()
#   claimants = models.ManyToManyField(Person, through='Claim')

    create_date = models.DateTimeField(
        default=timezone.now)
    # When the coupon becomes ready for use
    publish_date = models.DateTimeField(
        blank=True, null=True)
    # When this coupon expires
    end_date = models.DateTimeField(
        default=timezone.now)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    # Method to determine if coupon is currently published or not
    def published(self):
        return self.publish_date <= timezone.now() <= self.end_date
    published.admin_order_field = 'publish_date'
    published.boolean = True
    published.short_description = 'Published ?'

    # Human-readable name for Coupon
    def __str__(self):
        return self.title
