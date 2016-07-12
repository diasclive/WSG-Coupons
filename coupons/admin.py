from django.contrib import admin

from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    """fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['publish_date']}),
    ]"""
    list_display = ('title', 'code', 'published', 'publish_date')
    list_filter = ['publish_date']
    search_fields = ['title']

    def queryset(self, request):
        return Coupon.objects.filter(
            owner=request.user)

admin.site.register(Coupon, CouponAdmin)
