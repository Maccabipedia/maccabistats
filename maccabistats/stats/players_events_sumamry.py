# -*- coding: utf-8 -*-

# This class will handle all players events statistics.


class MaccabiGamesPlayersEventsSummaryStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats

    @property
    def total_goals_assists_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.best_assisters)

    @property
    def total_goals_scoring_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers)

    @property
    def total_penalties_goals_scoring_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_penalty)

    @property
    def total_freekicks_goals_scoring_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_freekick)

    @property
    def total_own_goals_scoring_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_own_goal)

    @property
    def total_head_goals_scoring_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.best_scorers_by_head)

    @property
    def total_goals_involved_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.most_goals_involved)

    @property
    def total_yellow_card_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.most_yellow_carded)

    @property
    def total_red_card_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.most_red_carded)

    @property
    def total_captains_counted_for_maccabi_players(self):
        return sum(player[1] for player in self.maccabi_games_stats.players.most_captains)

    def __str__(self):
        return f"Total event counting for maccabi players:\n\n" \
               f"   Goals: {self.total_goals_scoring_counted_for_maccabi_players}\n" \
               f"        By head: {self.total_head_goals_scoring_counted_for_maccabi_players}\n" \
               f"        By freekick: {self.total_freekicks_goals_scoring_counted_for_maccabi_players}\n" \
               f"        By penalty: {self.total_penalties_goals_scoring_counted_for_maccabi_players}\n" \
               f"        Own: {self.total_own_goals_scoring_counted_for_maccabi_players}\n" \
               f"   Assists: {self.total_goals_assists_counted_for_maccabi_players}\n" \
               f"   Goals involved: {self.total_goals_involved_counted_for_maccabi_players}\n" \
               f"   Cards:\n" \
               f"        Yellow cards: {self.total_yellow_card_counted_for_maccabi_players}\n" \
               f"        Red cards: {self.total_red_card_counted_for_maccabi_players}\n" \
               f"   Captains: {self.total_captains_counted_for_maccabi_players}\n"

    def __repr__(self):
        return str(self)

