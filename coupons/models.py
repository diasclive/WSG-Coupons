import datetime
import qrcode

from django.db import models
from django.utils import timezone
from django.urls import reverse

from accounts.models import Person
from WSG.settings import BASE_DIR, SITE_URL

def add_days():
    return timezone.now() + timezone.timedelta(days=7)

# Coupon Class Specifier
class Coupon(models.Model):
    owner = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        editable=False)
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    qr = models.ImageField(
        upload_to='static/qrcodes/',
        null=True,
        blank=True)
    terms = models.TextField()
    description = models.CharField(max_length=200)
    claimants = models.ManyToManyField(Person, through='Claim',
                                       related_name='Claimed')

    create_date = models.DateTimeField(
        default=timezone.now, editable=False)
    # When the coupon becomes ready for use
    publish_date = models.DateTimeField(
        default=timezone.now)
    # When this coupon expires
    expire_date = models.DateTimeField(
        default=add_days)
    '''
    # Use this method when we get to postgres
    expire_date = models.DurationField(
        default=datetime.timedelta(days=7), help_text="1 12:00 = 1 day + 12 hours")'''

    # Method to determine if coupon is currently published or not
    def published(self):
        return self.publish_date <= timezone.now() <= self.expire_date
    published.admin_order_field = 'publish_date'
    published.boolean = True
    published.short_description = 'Currently Running'

    def get_absolute_url(self):
        return reverse('coupons:detail', args=[str(self.id)])

    def gen_qrcode(self):
        if self.qr:
            self.qr.storage.delete(self.qr.path)

        qrc = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qrc.add_data(SITE_URL + self.get_absolute_url())
        qrc.make(fit=True)

        img = qrc.make_image()

        from django.core.files.uploadedfile import SimpleUploadedFile
        from io import BytesIO

        temp_handle = BytesIO()
        img.save(temp_handle, 'png')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(self.code,
                temp_handle.read(), content_type='image/png')

        self.qr.save(
            '%s.png' % self.code,
            suf,
            save=False
        )

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Coupon, self).save(*args, **kwargs)
        self.gen_qrcode()
        super(Coupon, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.qr.storage.delete(self.qr.path)
        super(Coupon, self).delete(*args, **kwargs)

    # Human-readable name for Coupon
    def __str__(self):
        return self.title

# Relationship between Coupon and User
class Claim(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_claimed = models.DateTimeField(
        default=timezone.now, editable=False)
