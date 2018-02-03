# -*- coding: utf-8 -*-

# This class will handle all results statistics.


class MaccabiGamesResultsStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.games = maccabi_games_stats.games

    @property
    def wins_count(self):
        return len([game for game in self.games if game.is_maccabi_win])

    @property
    def losses_count(self):
        return len([game for game in self.games if game.maccabi_score_diff < 0])

    @property
    def ties_count(self):
        return len([game for game in self.games if game.maccabi_score_diff == 0])
