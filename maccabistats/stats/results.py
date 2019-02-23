# -*- coding: utf-8 -*-

# This class will handle all results statistics.


class MaccabiGamesResultsStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.games = maccabi_games_stats.games

    @property
    def total_goals_against_maccabi(self):
        return sum([game.not_maccabi_team.score for game in self.games])

    @property
    def total_goals_for_maccabi(self):
        return sum([game.maccabi_score for game in self.games])

    @property
    def total_goals_diff_for_maccabi(self):
        return self.total_goals_for_maccabi - self.total_goals_against_maccabi

    @property
    def goals_ratio(self):
        """
         Goals for maccabi / Goals against maccabi
         """

        return round(self.total_goals_for_maccabi / self.total_goals_against_maccabi, 3)

    @property
    def wins_count(self):
        return len([game for game in self.games if game.is_maccabi_win])

    @property
    def wins_percentage(self):
        return round(self.wins_count / len(self.games), 3)

    @property
    def losses_count(self):
        return len([game for game in self.games if game.maccabi_score_diff < 0])

    @property
    def losses_percentage(self):
        return round(self.losses_count / len(self.games), 3)

    @property
    def ties_count(self):
        return len([game for game in self.games if game.maccabi_score_diff == 0])

    @property
    def ties_percentage(self):
        return round(self.ties_count / len(self.games), 3)

    @property
    def clean_sheets_count(self):
        return len([game for game in self.games if game.not_maccabi_team.score == 0])

    @property
    def clean_sheets_percentage(self):
        return round(self.clean_sheets_count / len(self.games), 3)
