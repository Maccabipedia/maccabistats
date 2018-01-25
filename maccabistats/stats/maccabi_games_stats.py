# -*- coding: utf-8 -*-


from itertools import groupby

from maccabistats.stats.coaches import MaccabiGamesCoachesStats
from maccabistats.stats.players import MaccabiGamesPlayersStats


class MaccabiGamesStats(object):

    def __init__(self, maccabi_site_games):
        """
        :type maccabi_site_games: list of maccabistats.models.game_data.GameData
        """

        self.games = sorted(maccabi_site_games, key=lambda g: g.date)  # Sort the games by date
        self.coaches = MaccabiGamesCoachesStats(self)
        self.players = MaccabiGamesPlayersStats(self)

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
        return set(game.competition for game in self.games)

    @property
    def maccabi_wins(self):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if game.is_maccabi_win])

    def get_games_against_team(self, team_name):
        """
        :param team_name: str.
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if team_name == game.not_maccabi_team.name])

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

    def get_first_league_games(self):
        """ Return only the first league games - from all years
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats(
            [game for game in self.games if game.competition in ["ליגת העל", "ליגת לאומית", "ליגת Winner", "ליגה א'"]])

    def get_longest_win_streak(self):
        """
        :rtype: int
        """
        maccabi_results = [game.is_maccabi_win for game in self.games]
        wins_streak = [len(list(streak_list)) for result, streak_list in groupby(maccabi_results) if result]
        return max(wins_streak)

    def get_longest_win_streak_with_games(self):
        """
        :return: int, list of maccabistats.models.game_data.GameData
        """
        maccabi_results = [game.is_maccabi_win for game in self.games]
        wins_streaks = [len(list(streak_list)) for result, streak_list in groupby(maccabi_results) if result]
        max_win_streak = max(wins_streaks)

        games_before_wins_streak = 0
        for result, current_results in groupby(maccabi_results):
            # Count only wins, if we reach the max wins streak we should stop!
            current_results_length = len(list(current_results))
            if result and max_win_streak == current_results_length:
                break
            else:
                games_before_wins_streak += current_results_length

        return max_win_streak, self.games[games_before_wins_streak: games_before_wins_streak + max_win_streak]

    def __len__(self):
        return len(self.games)

    def __getitem__(self, item):
        """
        :rtype: MaccabiSiteGameParser
        """
        return self.games[item]

    def __repr__(self):
        return "Contain {size} games".format(size=len(self))
