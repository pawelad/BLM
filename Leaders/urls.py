from django.conf.urls import patterns, url

from Leaders import views

urlpatterns = patterns(
    '',
    # ex: /leaders/
    url(r'^$', views.leaders_index, name='index'),
)
