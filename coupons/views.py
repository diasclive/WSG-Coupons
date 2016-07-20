from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Coupon, Claim
from accounts.models import Person

class IndexView(generic.ListView):
    template_name = 'coupons/index.html'
    context_object_name = 'latest_coupon_list'
    def get_queryset(self):
        """Return the last five published coupons."""
        return Coupon.objects.filter(
            publish_date__lte=timezone.now()
        ).order_by('-publish_date')[:5]

class DetailView(generic.DetailView):
    model = Coupon
    template_name = 'coupons/detail.html'
    def get_queryset(self):
        return Coupon.objects.filter(publish_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Coupon
    template_name = 'coupons/results.html'

def claim(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if request.user.is_authenticated():
        user = Person.objects.get(pk=request.user.id)
        if Claim.objects.filter(user=user, coupon=coupon).exists():
            # Redisplay the coupon detail form.
            return render(request, 'coupons/detail.html', {
                'coupon': coupon,
                'error_message': "You have already claimed this coupon.",
            })
        else:
            claim = Claim.objects.create(coupon=coupon, user=user)
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('coupons:index'))
    else:
        return render(request, 'coupons/detail.html', {
            'coupon': coupon,
            'error_message': "You need to be logged in to claim.",
        })
