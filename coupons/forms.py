from django import forms
from .models import Coupon
 
class CouponCreationForm(forms.ModelForm):
   
    class Meta:
        model = Coupon
        fields = ("title","code","description","publish_date","expire_date","terms")
        
    def __init__(self, *args, **kwargs):
        super(CouponCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        coupon = super(CouponCreationForm, self).save(commit=False)
        if commit:
            coupon.save()
        return coupon
