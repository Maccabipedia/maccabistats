# -*- coding: utf-8 -*-

# This class will handle all averages statistics.


class MaccabiGamesAverageStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.games = maccabi_games_stats.games

    @staticmethod
    def _prettify_averages(average):
        return float("{0:.2f}".format(average))

    @property
    def goals_for_maccabi(self):
        """
        :rtype: float
        """
        return MaccabiGamesAverageStats._prettify_averages(
            sum(game.maccabi_score for game in self.games) / len(self.games))

    @property
    def goals_against_maccabi(self):
        """
        :rtype: float
        """
        return MaccabiGamesAverageStats._prettify_averages(
            sum(game.not_maccabi_team.score for game in self.games) / len(self.games))

    @property
    def maccabi_diff(self):
        """
        :rtype: float
        """
        return MaccabiGamesAverageStats._prettify_averages(
            sum(game.maccabi_score_diff for game in self.games) / len(self.games))
