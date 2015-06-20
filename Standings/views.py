from django.shortcuts import render, get_list_or_404
from operator import itemgetter
from collections import OrderedDict

from Teams.models import Team


def standings_index(request):
    teams_list = get_list_or_404(Team)

    percentage_list = dict()
    for team in teams_list:
        percentage_list[team] = team.record()['percentage']

    # Sort team winning percentages
    percentage_list = OrderedDict(sorted(percentage_list.items(), key=itemgetter(1), reverse=True))
    best_team = next(iter(percentage_list))

    standings_list = OrderedDict()
    for team in percentage_list.keys():
        record = team.record()
        standings_list[team] = {
            'name': team.full_name, 'wins': record['wins'], 'loses': record['loses'],
            'percentage': percentage_list[team], 'gb': team.games_back(best_team),
            'home': team.record('home', display=True)['default'], 'away': team.record('away', display=True)['default']
        }

    return render(request, 'Standings/standings_index.html',
                  {'standings_list': standings_list})
