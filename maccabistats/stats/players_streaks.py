# -*- coding: utf-8 -*-

import logging

from progressbar import ProgressBar
from collections import defaultdict

logger = logging.getLogger(__name__)


# This class will handle all players streaks statistics.


class MaccabiGamesPlayersStreaksStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def _get_players_streak_by_condition(self, streak_condition, top_players_count=10):
        """
        For each player, filter only games that relevant for this player and calc streak_condition for the MaccabiGamesStats object.

        Example: "_get_players_streak_by_condition(lambda m: m.streaks.get_longest_unbeaten_streak_games())"

        :type streak_condition: callable (maccabistats.stats.maccabi_games_stats.MaccabiGamesStats)
        :param streak_condition: callable that get MaccabiGamesStats as param and return streak
        :type top_players_count: how many players to get (from the top)

        :rtype: list of (str, maccabistats.stats.maccabi_games_stats.MaccabiGamesStats)
        """

        pbar = ProgressBar()
        players_games = defaultdict(list)

        for game in pbar(self.games):
            for player in game.maccabi_team.played_players:
                players_games[player.name].append(game)

        for player in self.maccabi_games_stats.available_players:
            players_games[player.name] = self.maccabi_games_stats.create_maccabi_stats_from_games(players_games[player.name])

        unsorted_players_streaks = {player.name: streak_condition(players_games[player.name]) for player in self.maccabi_games_stats.available_players}
        return sorted(unsorted_players_streaks.items(), key=lambda kv: len(kv[1]), reverse=True)[:top_players_count]

    def get_players_with_best_unbeaten_streak(self):
        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_unbeaten_streak_games())

    def get_players_with_best_win_streak(self):
        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_wins_streak_games())

    def get_players_with_best_ties_streak(self):
        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_ties_streak_games())

    def get_players_with_best_losses_streak(self):
        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_losses_streak_games())

    def get_players_with_best_maccabi_score_goal_streak(self):
        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_score_at_least_games(1))

    def get_players_with_best_maccabi_score_at_least_goals_streak(self, goals_amount):
        """
        :param goals_amount: Goals amount that maccabi scored (at least)
        """

        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_score_at_least_games(goals_amount))

    def get_players_with_best_maccabi_score_no_goal_streak(self):
        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_score_exactly_games(0))

    def get_players_with_best_maccabi_score_exactly_goals_streak(self, goals_amount):
        """
        :param goals_amount: Goals amount that maccabi scored (exactly)
        """

        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_score_exactly_games(goals_amount))

    def get_players_with_best_clean_sheets_streak(self):
        return self._get_players_streak_by_condition(lambda m: m.streaks.get_longest_clean_sheet_games())
