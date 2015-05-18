from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from datetime import date


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

    def team_players(self):
        """Returns the list of players in the team"""
        from Players.models import Player

        team_players = list()
        for player in Player.objects.filter(team=self):
            team_players.append(player)

        return team_players

    def games_played(self):
        """Returns the number of games the team played"""
        from Games.models import TeamBoxscore

        today = date.today()

        return TeamBoxscore.objects.filter(team=self).filter(game__date__lte=today).count()

    def team_average_leader(self, stat):
        # TODO: Sort on base level (.extra)
        # TODO: Multiple players can have the same average
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.extra
        """Returns the player (and value) with best average in given statistic"""
        from Players.models import Player

        top_player = Player.objects.filter(team=self)[0]
        top_value = top_player.cat_average(stat)

        for player in Player.objects.filter(team=self):
            value = player.cat_average(stat)
            if value > top_value:
                top_player = player
                top_value = value

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

    def number_of_games(self):
        """Returns the number of games played by the team"""
        from Games.models import Game

        return Game.objects.team(self).count()

    def wins_loses(self, t, place='all'):
        """Returns the number of Team wins/loses (or record), with place of the game as second parameter"""
        from Games.models import Game

        if t not in ['wins', 'loses', 'record']:
            raise Exception("First parameter must be 'wins', 'loses' or 'record'")

        if place == 'all':
            games_list = Game.objects.team(self)
        elif place == 'home':
            games_list = Game.objects.filter(home_team=self)
        elif place == 'away':
            games_list = Game.objects.filter(away_team=self)
        else:
            raise Exception("Second parameter must be 'home' or 'away'")

        wins = 0
        loses = 0
        for game in games_list:
            if game.winner == self:
                wins += 1
            else:
                loses += 1

        if t == 'record':
            return '{wins} - {loses}'.format(wins=wins, loses=loses)
        else:
            return wins if t == 'wins' else loses

    def games_back(self, best_team):
        """Returns number of games back to given team"""
        return ((best_team.wins_loses('wins') - self.wins_loses('wins')) +
                (self.wins_loses('loses') - best_team.wins_loses('loses'))) / 2

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