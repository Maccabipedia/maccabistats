# -*- coding: utf-8 -*-

from pprint import pformat

from datetime import timedelta
from itertools import groupby, takewhile

from maccabistats.models.player_game_events import GameEventTypes


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

        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        games_fulfill_condition = [condition(game) for game in self.games]
        streak_by_condition = [len(list(streak_list)) for condition_fulfill, streak_list in
                               groupby(games_fulfill_condition) if condition_fulfill]

        if not streak_by_condition:  # In case were handling empty streak, just return empty list of games.
            return self.maccabi_games_stats.create_maccabi_stats_from_games([])

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

    def _get_similar_streaks(self, condition, minimum_streak_length=0):
        """
        :param condition: lambda which receive maccabistats.models.game_data.GameData as param and return bool.
        :type condition: callable
        :param minimum_streak_length: the size of the minimum streak to search for.
        :type minimum_streak_length: int

        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        games_fulfill_condition = [condition(game) for game in self.games]

        similar_streaks = []
        games_before_streak = 0

        for condition_fulfill, streak_list in groupby(games_fulfill_condition):
            # Count only if condition is true, if we reach the max streak we should stop!
            current_results_length = len(list(streak_list))
            if condition_fulfill and current_results_length >= minimum_streak_length:
                similar_streaks.append(self.maccabi_games_stats.create_maccabi_stats_from_games(
                    self.games[games_before_streak: games_before_streak + current_results_length]))

            games_before_streak += current_results_length

        return similar_streaks

    def _get_current_streak_by_condition(self, condition):
        """
        Returns the current streak of games which satisfies the condition

        :param condition: predicate to check for each game
        :type condition: callable

        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        current_streak = list(takewhile(condition, self.games[::-1]))
        return self.maccabi_games_stats.create_maccabi_stats_from_games(current_streak)

    def get_longest_wins_streak_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.is_maccabi_win)

    def get_similar_wins_streak_by_length(self, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.is_maccabi_win, minimum_streak_length=minimum_streak_length)

    def get_current_wins_streak(self):
        return self._get_current_streak_by_condition(lambda g: g.is_maccabi_win)

    def get_longest_ties_streak_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff == 0)

    def get_similar_ties_streak_by_length(self, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.maccabi_score_diff == 0, minimum_streak_length=minimum_streak_length)

    def get_current_ties_streak(self):
        return self._get_current_streak_by_condition(lambda g: g.maccabi_score_diff == 0)

    def get_longest_losses_streak_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff < 0)

    def get_similar_losses_streak_by_length(self, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.maccabi_score_diff < 0, minimum_streak_length=minimum_streak_length)

    def get_current_losses_streak(self):
        return self._get_current_streak_by_condition(lambda g: g.maccabi_score_diff < 0)

    def get_longest_unbeaten_streak_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff >= 0)

    def get_similar_unbeaten_streak_by_length(self, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.maccabi_score_diff >= 0, minimum_streak_length=minimum_streak_length)

    def get_current_unbeaten_streak(self):
        return self._get_current_streak_by_condition(lambda g: g.maccabi_score_diff >= 0)

    def get_longest_score_at_least_games(self, minimum_maccabi_score):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score >= minimum_maccabi_score)

    def get_similar_score_at_least_streak_by_length(self, minimum_maccabi_score, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.maccabi_score >= minimum_maccabi_score, minimum_streak_length=minimum_streak_length)

    def get_current_score_at_least_streak(self, minimum_maccabi_score):
        return self._get_current_streak_by_condition(lambda g: g.maccabi_score >= minimum_maccabi_score)

    def get_longest_score_exactly_games(self, maccabi_score):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score == maccabi_score)

    def get_current_score_exactly_streak(self, maccabi_score):
        return self._get_current_streak_by_condition(lambda g: g.maccabi_score == maccabi_score)

    def get_similar_score_exactly_streak_by_length(self, maccabi_score, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.maccabi_score == maccabi_score, minimum_streak_length=minimum_streak_length)

    def get_longest_score_diff_at_least_games(self, minimum_maccabi_score_diff):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff >= minimum_maccabi_score_diff)

    def get_similar_score_diff_at_least_streak_by_length(self, minimum_maccabi_score_diff, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.maccabi_score_diff >= minimum_maccabi_score_diff, minimum_streak_length=minimum_streak_length)

    def get_current_score_diff_at_least_streak(self, minimum_maccabi_score_diff):
        return self._get_current_streak_by_condition(lambda g: g.maccabi_score_diff >= minimum_maccabi_score_diff)

    def get_longest_score_diff_exactly_games(self, maccabi_score_diff):
        return self._get_longest_streak_by_condition(lambda g: g.maccabi_score_diff == maccabi_score_diff)

    def get_similar_score_diff_exactly_streak_by_length(self, maccabi_score_diff, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.maccabi_score_diff == maccabi_score_diff, minimum_streak_length=minimum_streak_length)

    def get_current_score_diff_exactly_streak(self, maccabi_score_diff):
        return self._get_current_streak_by_condition(lambda g: g.maccabi_score_diff == maccabi_score_diff)

    def get_longest_clean_sheet_games(self):
        return self._get_longest_streak_by_condition(lambda g: g.not_maccabi_team.score == 0)

    def get_similar_clean_sheet_streak_by_length(self, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.not_maccabi_team.score == 0, minimum_streak_length=minimum_streak_length)

    def get_current_clean_sheet_streak(self):
        return self._get_current_streak_by_condition(lambda g: g.not_maccabi_team.score == 0)

    def get_longest_scored_against_maccabi_not_more_than_games(self, not_maccabi_score):
        return self._get_longest_streak_by_condition(lambda g: g.not_maccabi_team.score <= not_maccabi_score)

    def get_longest_scored_against_maccabi_not_more_than_streak_by_length(self, not_maccabi_score, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: g.not_maccabi_team.score <= not_maccabi_score, minimum_streak_length=minimum_streak_length)

    def get_current_scored_against_maccabi_not_more_than_streak(self, not_maccabi_score):
        return self._get_current_streak_by_condition(lambda g: g.not_maccabi_team.score <= not_maccabi_score)

    def get_longest_goals_from_bench_games(self):
        return self._get_longest_streak_by_condition(lambda g: any(g.maccabi_team.has_goal_from_bench))

    def get_similar_goals_from_bench_streak_by_length(self, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: any(g.maccabi_team.has_goal_from_bench), minimum_streak_length=minimum_streak_length)

    def get_current_goals_from_bench_streak(self):
        return self._get_current_streak_by_condition(lambda g: any(g.maccabi_team.has_goal_from_bench))

    def get_longest_player_played_in_game(self, player_name):
        return self._get_longest_streak_by_condition(lambda g: player_name in g.maccabi_team.played_players_with_amount)

    def get_similar_player_played_in_game_streak_by_length(self, player_name, minimum_streak_length=0):
        return self._get_similar_streaks(lambda g: player_name in g.maccabi_team.played_players_with_amount,
                                         minimum_streak_length=minimum_streak_length)

    def get_current_player_played_in_game_streak(self, player_name):
        return self._get_current_streak_by_condition(lambda g: player_name in g.maccabi_team.played_players_with_amount)

    def _show_streaks(self):
        # TODO: this should be change to better way to design the streaks and the str\repr
        print(f"Longest streaks:\n"
              f"Wins streak: {self.get_longest_wins_streak_games()}\n"
              f"Similar wins streaks: {pformat(self.get_similar_wins_streak_by_length(len(self.get_longest_wins_streak_games())))})\n\n"
              f"Ties streak: {self.get_longest_ties_streak_games()}\n"
              f"Similar ties streaks: {pformat(self.get_similar_ties_streak_by_length(len(self.get_longest_ties_streak_games())))})\n\n"
              f"Losses streak: {self.get_longest_losses_streak_games()}\n"
              f"Similar ties streaks: {pformat(self.get_similar_losses_streak_by_length(len(self.get_longest_losses_streak_games())))})\n\n"
              f"Unbeaten streak: {self.get_longest_unbeaten_streak_games()}\n"
              f"Similar unbeaten streaks: {pformat(self.get_similar_unbeaten_streak_by_length(len(self.get_longest_unbeaten_streak_games())))})\n\n"
              f"Score goal streak: {self.get_longest_score_at_least_games(1)}\n"
              f"Similar score goal streaks: {pformat(self.get_similar_score_at_least_streak_by_length(1, len(self.get_longest_score_at_least_games(1))))})\n\n"
              f"No goal score streak: {self.get_longest_score_exactly_games(0)}\n"
              f"Similar no goal score streaks: {pformat(self.get_similar_score_exactly_streak_by_length(0, len(self.get_longest_score_exactly_games(0))))})\n\n"
              f"Clean sheet streak: {self.get_longest_clean_sheet_games()}\n"
              f"Similar Clean sheet streaks: {pformat(self.get_similar_clean_sheet_streak_by_length(len(self.get_longest_clean_sheet_games())))})\n\n"
              f"Goals from bench streak: {self.get_longest_goals_from_bench_games()}\n"
              f"Similar goals from bench streaks: {pformat(self.get_similar_goals_from_bench_streak_by_length(len(self.get_longest_goals_from_bench_games())))})\n\n"
              f"\n\nCurrent streaks:\n"
              f"Wins streak: {self.get_current_wins_streak()}\n"
              f"Ties streak: {self.get_current_ties_streak()}\n"
              f"Losses streak: {self.get_current_losses_streak()}\n"
              f"Unbeaten streak: {self.get_current_unbeaten_streak()}\n"
              f"Score goal streak: {self.get_current_score_at_least_streak(1)}\n"
              f"No goal score streak: {self.get_current_score_exactly_streak(0)}\n"
              f"Clean sheet streak: {self.get_current_clean_sheet_streak()}\n"
              f"Goals from bench streak: {self.get_current_goals_from_bench_streak()}\n"
              )

    def show_streaks(self):
        """
        Prints the best streak in many conditions (each functions of this class),
        For each streak show any similar streaks (if exists)
        """

        print("----------------------------------------------------\n### Overall streaks:\n\n")
        self._show_streaks()

        print("----------------------------------------------------\n### Home games streaks:\n\n")
        self.maccabi_games_stats.home_games.streaks._show_streaks()

        print("----------------------------------------------------\n### Away games streaks:\n\n")
        self.maccabi_games_stats.away_games.streaks._show_streaks()
