from django.contrib import admin

from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Information', {'fields': ['title','code','owner']}),
        ('Date Information', {'fields': ['create_date','publish_date','validity']}),
        ('Terms & Conditions', {'fields': ['terms']}),
    ]
    list_display = ('title', 'code', 'published', 'publish_date')
    list_filter = ['publish_date']
    search_fields = ['title']
    readonly_fields = ('create_date','owner',)
    save_as = True

    def queryset(self, request):
        return Coupon.objects.filter(
            owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
admin.site.register(Coupon, CouponAdmin)
