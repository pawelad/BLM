from django.db.models import Avg

from Games.models import PlayerBoxscore
from Players.models import Player


def stat_leaders(stat, n=5):
    """
    Returns a list of `n` leaders in given statistic
    """
    leaders_list = PlayerBoxscore.objects.exclude(
        min=0
    ).values(
        'player_id'
    ).annotate(
        stat_avg=Avg(stat)
    ).order_by(
        '-stat_avg'
    )

    leaders_list_parsed = list()
    for item in leaders_list[:n]:
        leaders_list_parsed.append({'player': Player.objects.get(id=item['player_id']),
                                    'value': '{0:.2f}'.format(item['stat_avg'])})

    return leaders_list_parsed
