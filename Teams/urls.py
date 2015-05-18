from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from Teams import views

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(pattern_name='home'), name='index'),
    # ex: /team/team_name/
    url(r'^(?P<team_name>\w+)/$', views.team_page, name='team_page'),
)