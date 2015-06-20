from collections import OrderedDict
from django.shortcuts import render

from Leaders.leaders import stat_leaders


def leaders_index(request):
    leaders_fields = [
        ['Minutes', 'Points', 'Assists',
         'Total Rebounds', 'Offensive Rebounds', 'Defensive Rebounds',
         'Steals', 'Blocks', 'Turnovers'],
        ['min', 'pts', 'ast',
         'reb_all', 'reb_off', 'reb_def',
         'stl', 'blk', 'to']
    ]

    all_stats_leaders = OrderedDict()
    for name, field in zip(leaders_fields[0], leaders_fields[1]):
        all_stats_leaders[name] = stat_leaders(field)

    return render(request, 'Leaders/leaders_index.html',
                  {'all_stats_leaders': all_stats_leaders})
