# -*- coding: utf-8 -*-


from itertools import groupby


# This class will handle all streaks statistics.


class MaccabiGamesStreaksStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def _get_longest_streak_by_condition(self, condition):
        """
        :param condition: lambda which receive maccabistats.models.game_data.GameData as param and return bool.
        :type condition: callable
        :return: list of maccabistats.models.game_data.GameData
        """

        games_fulfill_condition = [condition(game) for game in self.games]
        streak_by_condition = [len(list(streak_list)) for condition_fulfill, streak_list in
                               groupby(games_fulfill_condition) if condition_fulfill]
        max_streak_by_condition = max(streak_by_condition)

        games_before_streak = 0
        for condition_fulfill, streak_list in groupby(games_fulfill_condition):
            # Count only if condition is true, if we reach the max streak we should stop!
            current_results_length = len(list(streak_list))
            if condition_fulfill and max_streak_by_condition == current_results_length:
                break
            else:
                games_before_streak += current_results_length

        return self.maccabi_games_stats.create_maccabi_stats_from_games(
            self.games[games_before_streak: games_before_streak + max_streak_by_condition])

    def get_longest_wins_streak_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.is_maccabi_win)

    def get_longest_wins_streak_length(self):
        return len(self.get_longest_wins_streak_games())

    def get_longest_unbeaten_streak_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff >= 0)

    def get_longest_unbeaten_streak_length(self):
        return len(self.get_longest_unbeaten_streak_games())

    def get_longest_score_at_least_games(self, minimum_maccabi_score):
        """
        :type minimum_maccabi_score: int
        """
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score >= minimum_maccabi_score)

    def get_longest_score_at_least_length(self, minimum_maccabi_score):
        """
        :type minimum_maccabi_score: int
        """
        return len(self.get_longest_score_at_least_games(minimum_maccabi_score))

    def get_longest_score_exactly_games(self, maccabi_score):
        """
        :type maccabi_score: int
        """
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score == maccabi_score)

    def get_longest_score_exactly_length(self, maccabi_score):
        """
        :type maccabi_score: int
        """
        return len(self.get_longest_score_exactly_games(maccabi_score))

    def get_longest_score_diff_at_least_games(self, minimum_maccabi_score_diff):
        """
        :type minimum_maccabi_score_diff: int
        """
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff >= minimum_maccabi_score_diff)

    def get_longest_score_diff_at_least_length(self, minimum_maccabi_score_diff):
        """
        :type minimum_maccabi_score_diff: int
        """
        return len(self.get_longest_score_at_least_games(minimum_maccabi_score_diff))

    def get_longest_score_diff_exactly_games(self, maccabi_score_diff):
        """
        :type maccabi_score_diff: int
        """
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff == maccabi_score_diff)

    def get_longest_score_diff_exactly_length(self, maccabi_score_diff):
        """
        :type maccabi_score_diff: int
        """
        return len(self.get_longest_score_exactly_games(maccabi_score_diff))

    def get_longest_clean_sheet_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.not_maccabi_team.score == 0)

    def get_longest_clean_sheet_length(self):
        return len(self.get_longest_clean_sheet_games())
