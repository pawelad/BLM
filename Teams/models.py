from django.db import models
from django.db.models import Avg
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from datetime import date

from Games.models import PlayerBoxscore


class Coach(models.Model):
    first_name = models.CharField(
        verbose_name='First name',
        max_length=64,
    )

    last_name = models.CharField(
        verbose_name='Last name',
        max_length=64,
    )

    birth_date = models.DateField(
        verbose_name='Birth date',
    )

    @cached_property
    def full_name(self):
        """Example: Phil Jackson"""
        return '{first_name} {last_name}'.format(first_name=self.first_name,
                                                 last_name=self.last_name)

    def __str__(self):
        """Example: Phil Jackson (Chicago Bulls) / Phil Jackson"""
        try:
            return '{first_name} {last_name} ({team})'.format(first_name=self.first_name,
                                                              last_name=self.last_name,
                                                              team=self.team.full_name)
        except Team.DoesNotExist:
            return self.full_name

    def clean(self):
        if self.birth_date >= date.today():
            raise ValidationError({'birth_date': "Coach can't be born in the future."})


class Team(models.Model):
    # TODO: Add teams wins and losses to model ?

    full_name = models.CharField(
        verbose_name='Name',
        max_length=64,
    )

    short_name = models.CharField(
        verbose_name='Short name',
        max_length=5,
    )

    logo = models.ImageField(
        verbose_name='Logo',
        default='team_logos/default.png',
        upload_to='team_logos',
    )

    description = models.TextField(
        verbose_name='Description',
        max_length=1024,
        blank=True,
        default='',
    )

    coach = models.OneToOneField(
        'Teams.Coach', related_name='team',
        verbose_name='Coach',
    )

    captain = models.ForeignKey(
        'Players.Player', related_name='team_captain',
        verbose_name='Captain',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['full_name']

    @cached_property
    def count_players(self):
        """Returns the number of players on the team"""
        from Players.models import Player

        return Player.objects.filter(team=self).count()
    count_players.short_description = 'Number of players'

    def games_played(self):
        """Returns the number of games the team played"""
        from Games.models import Game

        return Game.objects.team(self).happened().count()

    def team_average_leader(self, stat):
        """Returns the player (and value) with best average in given statistic"""
        from Players.models import Player

        players_avg_list = PlayerBoxscore.objects.team(
            self
        ).exclude(
            min=0
        ).values(
            'player_id'
        ).annotate(
            stat_avg=Avg(stat)
        ).order_by(
            '-stat_avg'
        )

        top_value = '{0:.1f}'.format(players_avg_list[0]['stat_avg'])

        # Check if multiple players have the same average
        n = 1
        while players_avg_list[n-1] == players_avg_list[n]:
            n += 1

        if n == 1:
            top_player = Player.objects.get(id=players_avg_list[0]['player_id'])
        else:
            top_player = n

        return top_player, top_value

    def next_games(self, n):
        """Creates a list of `n` previous (if `n` is negative) or next (if `n` is positive) games of a team."""
        from Games.models import Game

        t = date.today()
        games_list = list()
        if n < 0:
            games = Game.objects.team(self).filter(date__lt=t).order_by('-date')[:-n]
        elif n > 0:
            games = Game.objects.team(self).filter(date__gte=t).order_by('date')[:n]
        else:
            raise Exception("Argument can't be 0")

        for game in games:
            games_list.append(game)

        return games_list

    def record(self, place='all', display=False):
        """Returns the number of Team wins, loses and the percentage in given place (home, away or all)"""
        from Games.models import Game

        games = Game.objects.happened()

        if place == 'all':
            wins = games.team(self).filter(winner=self).count()
            loses = games.team(self).exclude(winner=self).count()
        elif place == 'home':
            wins = games.filter(home_team=self).filter(winner=self).count()
            loses = games.filter(home_team=self).exclude(winner=self).count()
        elif place == 'away':
            wins = games.filter(away_team=self).filter(winner=self).count()
            loses = games.filter(away_team=self).exclude(winner=self).count()
        else:
            raise Exception("Place must be equal to 'home' or 'away'")

        try:
            percentage = float('{0:.3f}'.format(wins / self.games_played()))
        except ZeroDivisionError:
            return 0.0

        if display:
            return {'default': '{w} - {l}'.format(w=wins, l=loses),
                    'percentage': '{w} - {l} ({perc})'.format(w=wins, l=loses, perc=percentage)}
        else:
            return {'wins': wins, 'loses': loses, 'percentage': percentage}

    def games_back(self, best_team):
        """Returns number of games back to given team"""
        record = self.record()
        best_record = best_team.record()
        return ((best_record['wins'] - record['wins']) + (record['loses'] - best_record['loses'])) / 2

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('team:team_page', args=[str(self.full_name.replace(' ', '_'))])

    def __str__(self):
        """Example: Chicago Bulls (CHI)"""
        return '{full_name} ({short_name})'.format(full_name=self.full_name, short_name=self.short_name)

    def clean(self):
        if self.captain_id is not None and self.captain.team != self:
            raise ValidationError({'captain': "Team captain has to be in the team."})

        self.short_name = self.short_name.upper()
