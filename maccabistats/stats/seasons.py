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

    def sort_by_games_count(self):
        self._current_sort_attribute_function = lambda s: len(s)
        self._current_sort_attribute_description = "sort by games count"
        self.seasons = OrderedDict(sorted(self.seasons.items(), key=lambda item: self._current_sort_attribute_function(item[1]), reverse=True))

    def sort_by_wins_count(self):
        self._current_sort_attribute_function = lambda s: s.results.wins_count
        self._current_sort_attribute_description = "sort by wins count"
        self.seasons = OrderedDict(sorted(self.seasons.items(), key=lambda item: self._current_sort_attribute_function(item[1]), reverse=True))

    def sort_by_wins_percentage(self):
        self._current_sort_attribute_function = lambda s: s.results.wins_percentage
        self._current_sort_attribute_description = "sort by wins percentage"
        self.seasons = OrderedDict(sorted(self.seasons.items(), key=lambda item: self._current_sort_attribute_function(item[1]), reverse=True))

    def sort_by_avg_goals_diff(self):
        self._current_sort_attribute_function = lambda s: s.averages.maccabi_diff
        self._current_sort_attribute_description = "sort by average goal diff for maccabi"
        self.seasons = OrderedDict(sorted(self.seasons.items(), key=lambda item: self._current_sort_attribute_function(item[1]), reverse=True))

    def sort_by_avg_goals_for_maccabi(self):
        self._current_sort_attribute_function = lambda s: s.averages.goals_for_maccabi
        self._current_sort_attribute_description = "sort by average goals for maccabi"
        self.seasons = OrderedDict(sorted(self.seasons.items(), key=lambda item: self._current_sort_attribute_function(item[1]), reverse=True))

    def sort_by_avg_goals_against_maccabi(self):
        self._current_sort_attribute_function = lambda s: s.averages.goals_against_maccabi
        self._current_sort_attribute_description = "sort by average goals against maccabi"
        self.seasons = OrderedDict(sorted(self.seasons.items(), key=lambda item: self._current_sort_attribute_function(item[1]), reverse=True))


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
