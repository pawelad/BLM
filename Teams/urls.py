from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from Teams import views

urlpatterns = patterns(
    '',
    # ex: /team/team_name/
    url(r'^$', RedirectView.as_view(pattern_name='home'), name='index'),
    url(r'^(?P<team_name>\w+)/$', views.team_page, name='team_page'),
)