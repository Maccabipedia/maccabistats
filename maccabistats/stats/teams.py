# -*- coding: utf-8 -*-

import logging
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)


# This class will handle all teams statistics.


class MaccabiGamesTeamsStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.games = maccabi_games_stats.games
        self.maccabi_games_stats = maccabi_games_stats

    def __get_teams_sorted_by_most_of_this_condition(self, condition, top_teams_count=None, minimum_games_against_team=None):
        """
        Return Counter.most_common() of all the teams sorted by the results of this condition (Should be number) Desc.
        the condition receive MaccabiGamesStats which include only games against one team.

        :param condition: lambda team_games: team_games.results.wins_percentage, which will return the teams order by the win percentage for maccabi.
        :type condition: callable
        :type top_teams_count: how many teams to get (from the top)
        :param minimum_games_against_team: include only teams with minimum number of games against them
        :type minimum_games_against_team: int
        :return: list of tuple
        """
        top_teams_count = top_teams_count or 20
        minimum_games_against_team = minimum_games_against_team or 0
        teams_games = defaultdict(list)

        for game in self.games:
            teams_games[game.not_maccabi_team.name].append(game)

        teams_with_condition = {}
        for team_name in teams_games.keys():
            if len(teams_games[team_name]) >= minimum_games_against_team:
                teams_with_condition[team_name] = condition(self.maccabi_games_stats.create_maccabi_stats_from_games(teams_games[team_name]))
            else:
                logger.debug(f"Ignoring {team_name} in this calculation, "
                             f"required games length is: {minimum_games_against_team}, team games length: {len(teams_games[team_name])}")

        return Counter(teams_with_condition).most_common()[:top_teams_count]

    def teams_ordered_by_maccabi_wins(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.wins_count, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_maccabi_wins_percentage(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.wins_percentage, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_maccabi_losses(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.losses_count, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_maccabi_losses_percentage(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.losses_percentage, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_wins_minus_losses(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.wins_count - t.results.losses_count,
                                                                 top_teams_count, minimum_games_against_team)

    def teams_ordered_by_maccabi_ties(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.ties_count, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_maccabi_ties_percentage(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.ties_percentage, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_maccabi_clean_sheets_count(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.clean_sheets_count, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_maccabi_clean_sheets_percentage(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.clean_sheets_percentage,
                                                                 top_teams_count, minimum_games_against_team)

    def teams_ordered_by_goals_ratio(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.goals_ratio, top_teams_count, minimum_games_against_team)

    def teams_ordered_by_goals_diff(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.total_goals_diff_for_maccabi,
                                                                 top_teams_count, minimum_games_against_team)

    def teams_ordered_by_total_goals_for_maccabi(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.total_goals_for_maccabi,
                                                                 top_teams_count, minimum_games_against_team)

    def teams_ordered_by_total_goals_against_maccabi(self, top_teams_count=None, minimum_games_against_team=None):
        return self.__get_teams_sorted_by_most_of_this_condition(lambda t: t.results.total_goals_against_maccabi,
                                                                 top_teams_count, minimum_games_against_team)
