# -*- coding: utf-8 -*-

import logging

from progressbar import ProgressBar
from collections import defaultdict

logger = logging.getLogger(__name__)


# This class will handle all teams streaks statistics.


class MaccabiGamesTeamsStreaksStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def _get_team_streak_by_condition(self, streak_condition, top_teams_count=20):
        """
        For each team, filter only games that relevant for this team and calc streak_condition for the MaccabiGamesStats object.

        :type streak_condition: callable (maccabistats.stats.maccabi_games_stats.MaccabiGamesStats, str)
        :param streak_condition: callable that get MaccabiGamesStats and return the games which match the condition
        :type top_teams_count: how many teams to get (from the top)

        :rtype: list of (str, maccabistats.stats.maccabi_games_stats.MaccabiGamesStats)
        """

        teams_games = defaultdict(list)

        for game in self.games:
            teams_games[game.not_maccabi_team.name].append(game)

        for team_name in teams_games.keys():
            # TODO : should consider change this design, that condition gets the MaccabiGameStats, that in this way to match the players streaks.
            teams_games[team_name] = streak_condition(self.maccabi_games_stats.create_maccabi_stats_from_games(teams_games[team_name]))

        return sorted(teams_games.items(), key=lambda team_name_to_games: len(team_name_to_games[1]), reverse=True)[:top_teams_count]

    def get_teams_with_best_unbeaten_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_unbeaten_streak_games())

    def get_teams_with_best_win_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_wins_streak_games())

    def get_teams_with_best_ties_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_ties_streak_games())

    def get_teams_with_best_losses_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_losses_streak_games())

    def get_teams_with_best_maccabi_score_goal_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_score_at_least_games(1))

    def get_teams_with_best_maccabi_score_at_least_goals_streak(self, goals_amount):
        """
        :param goals_amount: Goals amount that maccabi scored (at least)
        """

        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_score_at_least_games(goals_amount))

    def get_teams_with_best_maccabi_score_no_goal_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_score_exactly_games(0))

    def get_teams_with_best_maccabi_score_exactly_goals_streak(self, goals_amount):
        """
        :param goals_amount: Goals amount that maccabi scored (exactly)
        """

        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_score_exactly_games(goals_amount))

    def get_teams_with_best_clean_sheets_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_longest_clean_sheet_games())
    
    # Current streaks:
    def get_teams_with_current_unbeaten_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_unbeaten_streak())

    def get_teams_with_current_win_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_wins_streak())

    def get_teams_with_current_ties_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_ties_streak())

    def get_teams_with_current_losses_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_losses_streak())

    def get_teams_with_current_maccabi_score_goal_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_score_at_least_streak(1))

    def get_teams_with_current_maccabi_score_at_least_goals_streak(self, goals_amount):
        """
        :param goals_amount: Goals amount that maccabi scored (at least)
        """

        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_score_at_least_streak(goals_amount))

    def get_teams_with_current_maccabi_score_no_goal_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_score_exactly_streak(0))

    def get_teams_with_current_maccabi_score_exactly_goals_streak(self, goals_amount):
        """
        :param goals_amount: Goals amount that maccabi scored (exactly)
        """

        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_score_exactly_streak(goals_amount))

    def get_teams_with_current_clean_sheets_streak(self):
        return self._get_team_streak_by_condition(lambda games: games.streaks.get_current_clean_sheet_streak())


