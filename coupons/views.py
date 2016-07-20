from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Coupon, Claim

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

def claim(request, coupon_code):
    coupon = get_object_or_404(Coupon, pk=coupon_code)
    try:
        user = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Person.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'coupons/detail.html', {
            'coupon': coupon,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
