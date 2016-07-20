from django.conf.urls import url

from . import views

app_name = 'coupons'
urlpatterns = [
    # ex: /coupons/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /coupons/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /coupons/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /coupons/5/claim/
    url(r'^(?P<coupon_id>[0-9]+)/claim/$', views.claim, name='claim'),
]
