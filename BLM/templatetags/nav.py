from django import template
from django.core.urlresolvers import reverse

from Teams.models import Team

register = template.Library()


@register.inclusion_tag('partials/nav.html', takes_context=True)
def nav(context):
    links = [{'name': 'Home', 'url': reverse('home')},
             {'name': 'Teams', 'url': reverse('team:index')},
             {'name': 'Players', 'url': reverse('player:index')},
             {'name': 'Games', 'url': reverse('game:index')}]

    all_teams = list()
    for team in Team.objects.all():
        all_teams.append(team)

    path = context['request'].path

    return {'links': links, 'all_teams': all_teams, 'path': path}