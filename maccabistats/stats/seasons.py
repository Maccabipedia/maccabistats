# -*- coding: utf-8 -*-
import logging
import pprint
from collections import OrderedDict

logger = logging.getLogger(__name__)


# TODO think about inherit form ordereddict
class Seasons(object):
    """
    This class is responsible for maccabi seasons manipulating, such as sorting by wins count, goals for maccabi and so on.

    The pattern for adding "sort_by" function is to add lambda which receive just the season maccabi games stats object,
    inside the function itself you should set the key with lambda that 'removes' the season string.
    example function - sort_by_wins_count.
    """

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """
        self.maccabi_games_stats = maccabi_games_stats

        all_seasons = self.maccabi_games_stats.available_seasons
        self.seasons = OrderedDict({season: self.maccabi_games_stats.get_games_by_season(season) for season in all_seasons})

        # sort attribute use to show the relevant data after sorting.
        self._current_sort_attribute_function = lambda s: ""
        self._current_sort_attribute_description = "order by season number"

    def __repr__(self):
        ordered_seasons = pprint.pformat(["{season} ({value})".
                                         format(season=season, value=self._current_sort_attribute_function(self[season]))
                                          for season in list(self.seasons.keys())])

        return "{description}: \n\n{ordered_seasons}".format(description=self._current_sort_attribute_description, ordered_seasons=ordered_seasons)

    def __len__(self):
        return len(self.seasons)

    def __getitem__(self, item):
        """
        Allow to use ['1990-91'] or by indexing [0]
        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """
        if isinstance(item, str):
            return self.seasons[item]
        else:
            return list(self.seasons.items())[item][1]

    def _refresh_sorting(self, sort_attribute_function, sort_attribute_description):
        """
        Updates the current sorting, all the seasons will be sorted using the given callable (gets a seasons item - MaccabiGamesStats).
        :param sort_attribute_function: The callable to sort the seasons by (gets season item - MaccabiGamesStats)
        :type sort_attribute_function: callable
        :param sort_attribute_description: The description wich will be shown when sorting
        :type sort_attribute_description: basestring
        """
        self._current_sort_attribute_function = sort_attribute_function
        self._current_sort_attribute_description = sort_attribute_description
        self.seasons = OrderedDict(sorted(self.seasons.items(), key=lambda item: self._current_sort_attribute_function(item[1]), reverse=True))

    # Games Results:
    def sort_by_games_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: len(s), sort_attribute_description="sort by games count")

    def sort_by_wins_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.wins_count, sort_attribute_description="sort by wins count")

    def sort_by_wins_percentage(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.wins_percentage, sort_attribute_description="sort by wins percentage")

    def sort_by_losses_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.losses_count, sort_attribute_description="sort by losses count")

    def sort_by_losses_percentage(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.losses_percentage, sort_attribute_description="sort by losses percentage")

    def sort_by_ties_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.ties_count, sort_attribute_description="sort by ties count")

    def sort_by_ties_percentage(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.ties_percentage, sort_attribute_description="sort by ties percentage")

    # Goals manipulations:
    def sort_by_total_goals_diff(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.total_goals_diff_for_maccabi,
                              sort_attribute_description="sort by total goals diff for maccabi")

    def sort_by_average_goals_diff_per_game(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.averages.maccabi_diff,
                              sort_attribute_description="sort by average (per game) goal diff for maccabi")

    def sort_by_total_goals_for_maccabi(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.total_goals_for_maccabi,
                              sort_attribute_description="sort by total goals for maccabi")

    def sort_by_average_goals_for_maccabi_per_game(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.averages.goals_for_maccabi,
                              sort_attribute_description="sort by average goals (per game) for maccabi")

    def sort_by_total_goals_against_maccabi(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.total_goals_against_maccabi,
                              sort_attribute_description="sort by total goals against maccabi")

    def sort_by_average_goals_against_maccabi_per_game(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.averages.goals_against_maccabi,
                              sort_attribute_description="sort by average goals (per game) against maccabi")

    def sort_by_clean_sheet_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.clean_sheets_count, sort_attribute_description="sort by clean sheets count")

    def sort_by_clean_sheet_percentage(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.clean_sheets_percentage,
                              sort_attribute_description="sort by clean sheets percentage")

    def sort_by_goals_ratio(self):
        """
        Goals for maccabi / Goals against maccabi
        """
        self._refresh_sorting(sort_attribute_function=lambda s: s.results.goals_ratio,
                              sort_attribute_description="sort by goals ratio (Goals for maccabi / Goals against maccabi)")

    def sort_by_home_players_goals_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.players_categories.home_players_goals_count(),
                              sort_attribute_description="sort by home players goals count")

    def sort_by_home_players_goals_ratio(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.players_categories.home_players_goals_ratio(),
                              sort_attribute_description="sort by home players goals ratio")

    def sort_by_home_players_assists_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.players_categories.home_players_assists_count(),
                              sort_attribute_description="sort by home players assists count")

    def sort_by_home_players_assists_ratio(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.players_categories.home_players_assists_ratio(),
                              sort_attribute_description="sort by home players assists ratio")

    def sort_by_home_players_goals_involved_count(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.players_categories.home_players_goals_involved_count(),
                              sort_attribute_description="sort by home players goals involved count")

    def sort_by_home_players_goals_involved_ratio(self):
        self._refresh_sorting(sort_attribute_function=lambda s: s.players_categories.home_players_goals_involved_ratio(),
                              sort_attribute_description="sort by home players goals involved ratio")


# This class will handle all seasons statistics.


class MaccabiGamesSeasonsStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def get_seasons_stats(self):
        return Seasons(self.maccabi_games_stats)
