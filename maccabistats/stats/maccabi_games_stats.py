# -*- coding: utf-8 -*-


from maccabistats.stats.coaches import MaccabiGamesCoachesStats
from maccabistats.stats.players import MaccabiGamesPlayersStats
from maccabistats.stats.streaks import MaccabiGamesStreaksStats
from maccabistats.stats.averages import MaccabiGamesAverageStats
from maccabistats.stats.referees import MaccabiGamesRefereesStats

from maccabistats.stats.results import MaccabiGamesResultsStats
from maccabistats.version import version as maccabistats_version


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

    def get_first_league_games(self):
        """ Return only the first league games - from all years
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats(
            [game for game in self.games if game.competition in ["ליגת העל", "ליגת לאומית", "ליגת Winner", "ליגה א'"]])

    @staticmethod
    def create_maccabi_stats_from_games(games):
        """ Creates MaccabiGamesStats from list of maccabistats.models.game_data.GameData
        :param games: list of maccabistats.models.game_data.GameData
        :return: MaccabiGamesStats
        """

        return MaccabiGamesStats(games)

    def __len__(self):
        return len(self.games)

    def __getitem__(self, item):
        """
        :rtype: MaccabiSiteGameParser
        """
        return self.games[item]

    def __repr__(self):
        return "Contain {size} games".format(size=len(self))
