# -*- coding: utf-8 -*-


from maccabistats.stats.coaches import MaccabiGamesCoachesStats
from maccabistats.stats.players import MaccabiGamesPlayersStats
from maccabistats.stats.streaks import MaccabiGamesStreaksStats
from maccabistats.stats.averages import MaccabiGamesAverageStats
from maccabistats.stats.referees import MaccabiGamesRefereesStats
from maccabistats.stats.comebacks import MaccabiGamesComebacksStats
from maccabistats.stats.seasons import MaccabiGamesSeasonsStats
from maccabistats.stats.results import MaccabiGamesResultsStats
from maccabistats.stats.important_goals import MaccabiGamesImportantGoalsStats
from maccabistats.stats.graphs import MaccabiGamesGraphsStats

from maccabistats.version import version as maccabistats_version

from dateutil.parser import parse as datetime_parser
from tempfile import NamedTemporaryFile
import datetime
import json
import logging

logger = logging.getLogger(__name__)


class MaccabiGamesStats(object):

    def __init__(self, maccabi_site_games):
        """
        :type maccabi_site_games: list of maccabistats.models.game_data.GameData
        """

        self.games = sorted(maccabi_site_games, key=lambda g: g.date)  # Sort the games by date

        self.coaches = MaccabiGamesCoachesStats(self)
        self.players = MaccabiGamesPlayersStats(self)
        self.streaks = MaccabiGamesStreaksStats(self)
        self.averages = MaccabiGamesAverageStats(self)
        self.results = MaccabiGamesResultsStats(self)
        self.referees = MaccabiGamesRefereesStats(self)
        self.comebacks = MaccabiGamesComebacksStats(self)
        self.seasons = MaccabiGamesSeasonsStats(self)
        self.important_goals = MaccabiGamesImportantGoalsStats(self)
        self.graphs = MaccabiGamesGraphsStats(self)

        self.version = maccabistats_version

    @property
    def home_games(self):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if game.is_maccabi_home_team])

    @property
    def away_games(self):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if not game.is_maccabi_home_team])

    @property
    def available_competitions(self):
        return list(set(game.competition for game in self.games))

    @property
    def available_opponents(self):
        return list(set(game.not_maccabi_team.name for game in self.games))

    @property
    def available_stadiums(self):
        return list(set(game.stadium for game in self.games))

    @property
    def available_players(self):
        players = []
        [players.extend(game.maccabi_team.players) for game in self.games]

        return list(set([player.get_as_normal_player() for player in players]))

    @property
    def available_referees(self):
        return list(set(game.referee for game in self.games))

    @property
    def available_coaches(self):
        return list(set(game.maccabi_team.coach for game in self.games))

    @property
    def available_seasons(self):
        return sorted(list(set(game.season for game in self.games)))

    @property
    def maccabi_wins(self):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if game.is_maccabi_win])

    def played_before(self, date):
        return MaccabiGamesStats([game for game in self.games if game.played_before(date)])

    def played_after(self, date):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if game.played_after(date)])

    def played_at(self, date):
        """
        Currently checking just the: year & month & day.
        :param date: datetime.datetime or str
        :rtype: list of maccabistats.models.game_data.GameData
        """

        if type(date) is str:
            date = datetime_parser(date).date()
        elif type(date) is datetime.datetime:
            date = date.date()  # Leave only year & month & day

        return [game for game in self.games if game.date.date() == date]

    def get_games_by_competition(self, competition_types):
        """
        :type competition_types: str or list of str
        :rtype: MaccabiGamesStats
        """

        if type(competition_types) is str:
            competition_types = [competition_types]

        return MaccabiGamesStats([game for game in self.games if game.competition in competition_types])

    def get_games_by_stadium(self, stadium_name):
        """
        :param stadium_name: str.
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if stadium_name == game.stadium])

    def get_games_against_team(self, team_name):
        """
        :param team_name: str.
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if team_name == game.not_maccabi_team.name])

    def get_games_by_coach(self, coach_name):
        """
        :param coach_name: str.
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if coach_name == game.maccabi_team.coach])

    def get_games_by_referee(self, referee_name):
        """
        :param referee_name: str.
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if referee_name == game.referee])

    def get_games_by_player_name(self, player_name):
        """
        :param player_name: str.
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games
                                  if player_name in [p.name.strip() for p in game.maccabi_team.played_players]])

    def get_games_by_season(self, season):
        """
        Return Maccabi games stats object with season games, season may be entered as "1900/01".
        :param season: season to get game for.
        :rtype: MaccabiGamesStats
        """

        return MaccabiGamesStats([game for game in self.games if game.season == season])

    def get_first_league_games(self):
        """ Return only the first league games - from all years
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats(
            [game for game in self.games if game.competition in ["ליגת העל", "ליגה לאומית", "ליגת Winner", "ליגה א'", "ליגה א"]])

    @staticmethod
    def create_maccabi_stats_from_games(games):
        """ Creates MaccabiGamesStats from list of maccabistats.models.game_data.GameData
        :param games: list of maccabistats.models.game_data.GameData
        :return: MaccabiGamesStats
        """

        return MaccabiGamesStats(games)

    def get_players_by_name(self, player_name):
        """
        Return list of players which *CONTAINS* the player_name param.
        :param player_name: name to search in all players name list.
        :return: list of maccabistats.models.player_in_game.PlayerInGame
        """

        return [player for player in self.available_players if player_name in player.name]

    def get_summary(self):
        summary = {'games': len(self),
                   "wins": self.results.wins_count,
                   "wins_by_percentage": self.results.wins_percentage,
                   "losses": self.results.losses_count,
                   "losses_by_percentage": self.results.losses_percentage,
                   "ties": self.results.ties_count,
                   "ties_by_percentage": self.results.ties_percentage,
                   "goals_for_maccabi": self.results.total_goals_for_maccabi,
                   "goals_for_maccabi_avg": self.averages.goals_for_maccabi,
                   "goals_against_maccabi": self.results.total_goals_against_maccabi,
                   "goals_against_maccabi_avg": self.averages.goals_against_maccabi,
                   "goals_diff_for_maccabi": self.results.total_goals_diff_for_maccabi,
                   "goals_diff_for_maccabi_avg": self.averages.maccabi_diff}

        return summary

    def show_sumamry(self):
        summary = ("Maccabi games stats object:"
                   "\n\nGames count: {games}"
                   "\nWins : {wins} ({wins_by_percentage}%)"
                   "\nLosses : {losses} ({losses_by_percentage}%)"
                   "\nTies : {ties} ({ties_by_percentage}%)"
                   "\n\nGoals for maccabi : {goals_for_maccabi}, {goals_for_maccabi_avg} per game"
                   "\nGoals against maccabi : {goals_against_maccabi}, {goals_against_maccabi_avg} per game"
                   "\nGoals diff for maccabi: {goals_diff_for_maccabi}, {goals_diff_for_maccabi} per game").format(**self.get_summary())

        print(summary)

    def to_json(self):
        return json.dumps([game.to_json() for game in self.games], indent=4)

    def json_to_temp_file(self):
        # TODO, there is too much escaped stuff in this function output
        with NamedTemporaryFile(delete=False, mode='w') as temp_json:
            logger.info(f"Serializing current maccabi games stats to temporary json file at: {temp_json.name}")
            temp_json.file.write(self.to_json())

    def __len__(self):
        return len(self.games)

    def __getitem__(self, item):
        """
        :rtype: maccabistats.models.game_data.GameData
        """
        return self.games[item]

    def __repr__(self):
        summary = "Contains {size} games".format(size=len(self))
        if len(self) > 0:
            summary += "(from {start_date} to {end_date})".format(start_date=self[0].date.strftime('%d-%m-%Y'),
                                                                  end_date=self[-1].date.strftime('%d-%m-%Y'))

        return summary
