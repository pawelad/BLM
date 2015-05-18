from django.shortcuts import render, get_list_or_404
from operator import itemgetter
from collections import OrderedDict

from Teams.models import Team


def standings_index(request):
    teams_list = get_list_or_404(Team)

    percentage_list = dict()
    for team in teams_list:
        percentage_list[team] = team.wins_loses('wins') / team.number_of_games()

    # Sort team winning percentages
    percentage_list = OrderedDict(sorted(percentage_list.items(), key=itemgetter(1), reverse=True))
    best_team = next(iter(percentage_list))

    standings_list = OrderedDict()
    for team in percentage_list.keys():
        standings_list[team] = {
            'name': team.full_name, 'wins': team.wins_loses('wins'), 'loses': team.wins_loses('loses'),
            'percentage': '{0:.3f}'.format(percentage_list[team]), 'gb': team.games_back(best_team),
            'home': team.wins_loses('record', 'home'), 'away': team.wins_loses('record', 'away')
        }

    return render(request, 'Standings/standings_index.html',
                  {'standings_list': standings_list})