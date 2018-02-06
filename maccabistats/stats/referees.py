# -*- coding: utf-8 -*-

from collections import Counter


# This class will handle all referees statistics.


class MaccabiGamesRefereesStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.games = maccabi_games_stats.games

    @property
    def most_judged_referee(self):
        """
        :rtype: Counter
        """
        return Counter(game.referee for game in self.games).most_common()

    @property
    def best_referee(self):
        """
        :rtype: Counter
        """
        return Counter(game.referee for game in self.games if game.is_maccabi_win).most_common()

    @property
    def worst_referee(self):
        """
        :rtype: Counter
        """
        return Counter(game.referee for game in self.games if game.maccabi_score_diff < 0).most_common()

    @property
    def best_referee_by_percentage(self):
        """
        :rtype: Counter
        """

        # Both return as Counter.most_common() which is list (of tuples)
        judged_games = Counter(dict(self.most_judged_referee))
        games_won_with_referees = Counter(dict(self.best_referee))

        best_referee = Counter()
        for referee_name, judged_times in judged_games.items():
            key_name = "{referee} - {judged}".format(referee=referee_name, judged=judged_times)
            best_referee[key_name] = round(games_won_with_referees[referee_name] / judged_times * 100, 2)

        return best_referee.most_common()

    @property
    def worst_referee_by_percentage(self):
        """
        :rtype: Counter
        """

        # Both return as Counter.most_common() which is list (of tuples)
        judged_games = Counter(dict(self.most_judged_referee))
        games_lost_with_referees = Counter(dict(self.worst_referee))

        best_referee = Counter()
        for referee_name, judged_times in judged_games.items():
            key_name = "{referee} - {judged}".format(referee=referee_name, judged=judged_times)
            best_referee[key_name] = round(games_lost_with_referees[referee_name] / judged_times * 100, 2)

        return best_referee.most_common()
