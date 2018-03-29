from difflib import SequenceMatcher
from itertools import permutations

SIMILARITY_MINIMAL_RATIO = 0.9


class NamingErrorsFinder(object):
    """
    This class is responsible for trying find similar names for each attribute of MaccabiGamesStats like:
    player named "avi nimni" and "avi nimmni" and so on.

    ratio = 1.0 wont be print because we use set for all objects.
    """

    def __init__(self, maccabi_games_stats, minimal_ratio_to_alert=SIMILARITY_MINIMAL_RATIO):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        :param minimal_ratio_to_alert: the minimum ratio to report about naming similarity for.
        :type: float
        """

        self.games = maccabi_games_stats
        self.minimal_ratio = minimal_ratio_to_alert

    def print_naming_similarities(self):
        """
        Check for all naming errors and print them!
        """

        self.__print_coaches_naming_similarities()
        self.__print_referees_naming_similarities()
        self.__print_opponents_naming_similarities()
        self.__print_stadiums_naming_similarities()
        self.__print_players_naming_similarities()

    # We use set to reduce duplication of the same players (or other object that are equal).
    def __print_coaches_naming_similarities(self):
        self.__print_couples_naming_similarity(permutations(set(self.games.available_coaches), 2), "Coaches")

    def __print_referees_naming_similarities(self):
        self.__print_couples_naming_similarity(permutations(set(self.games.available_referees), 2), "Referees")

    def __print_opponents_naming_similarities(self):
        self.__print_couples_naming_similarity(permutations(set(self.games.available_opponents), 2), "Opponents")

    def __print_stadiums_naming_similarities(self):
        self.__print_couples_naming_similarity(permutations(set(self.games.available_stadiums), 2), "Stadiums")

    def __print_players_naming_similarities(self):
        self.__print_couples_naming_similarity(permutations(set([p.name for p in self.games.available_players]), 2), "Players")

    def __print_couples_naming_similarity(self, couples_permutations, prefix_to_print):
        for couple in couples_permutations:
            current_ratio = self.__similarity_of_two_names(*couple)
            if current_ratio > self.minimal_ratio:
                print("{prefix}: {} - {}, ratio - {ratio}".format(prefix=prefix_to_print, *couple, ratio=round(current_ratio, 2)))

    @staticmethod
    def __similarity_of_two_names(first, second):
        """
        Check the similarity of two names, returns the similarity between 0 and 1.
        :type first: str
        :type second: str
        :rtype: float
        """

        return SequenceMatcher(None, first, second).ratio()
