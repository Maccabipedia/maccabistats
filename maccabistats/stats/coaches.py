# -*- coding: utf-8 -*-

from collections import Counter


# This class will handle all coaches statistics.


class MaccabiGamesCoachesStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats
        self.games = self.maccabi_games_stats.games

    @property
    def most_trained_coach(self):
        """
        :rtype: Counter
        """
        return Counter(game.maccabi_team.coach for game in self.games).most_common()

    @property
    def most_winner_coach(self):
        """
        :rtype: Counter
        """
        return Counter(game.maccabi_team.coach for game in self.games if game.is_maccabi_win).most_common()

    @property
    def most_loser_coach(self):
        """
        :rtype: Counter
        """
        return Counter(game.maccabi_team.coach for game in self.games if game.maccabi_score_diff < 0).most_common()

    @property
    def most_winner_coach_by_percentage(self):
        """
        :rtype: Counter
        """

        # Both return as Counter.most_common() which is list (of tuples)
        trained_games = Counter(dict(self.most_trained_coach))
        games_won = Counter(dict(self.most_winner_coach))

        best_coach = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            best_coach[key_name] = round(games_won[coach_name] / trained_times * 100, 2)

        return best_coach.most_common()

    @property
    def most_loser_coach_by_percentage(self):
        """
        :rtype: Counter
        """

        # Both return as Counter.most_common() which is list (of tuples)
        trained_games = Counter(dict(self.most_trained_coach))
        games_lost = Counter(dict(self.most_loser_coach))

        worst_coach = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            worst_coach[key_name] = round(games_lost[coach_name] / trained_times * 100, 2)

        return worst_coach.most_common()
