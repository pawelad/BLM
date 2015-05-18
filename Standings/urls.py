from django.conf.urls import patterns, url

from Standings import views

urlpatterns = patterns(
    '',
    # ex: /standings/
    url(r'^$', views.standings_index, name='index'),
)