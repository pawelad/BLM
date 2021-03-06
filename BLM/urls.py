from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from BLM import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^player/', include('Players.urls', namespace='player')),
    url(r'^team/', include('Teams.urls', namespace='team')),
    url(r'^game/', include('Games.urls', namespace='game')),
    url(r'^standings/', include('Standings.urls', namespace='standings')),
    url(r'^leaders/', include('Leaders.urls', namespace='leaders')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
