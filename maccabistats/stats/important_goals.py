# -*- coding: utf-8 -*-

from datetime import timedelta
from collections import Counter


# This class will handle all important goals statistics.


class MaccabiGamesImportantGoalsStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def get_top_scorers_for_advantage(self):
        """
        Get all players who score goal that made maccabi the lead team AFTER the goal was scored.
        """

        return self.get_top_scorers(1, 1)

    def get_top_scorers(self, minimum_diff_for_maccabi=-2, maximum_diff_for_maccabi=1, goal_condition=None):
        if goal_condition is None:
            goal_condition = lambda x: True

        maccabi_goals = [goal for game in self.games for goal in game.goals() if goal['team'] == "מכבי תל אביב"]
        maccabi_important_goals = [goal for goal in maccabi_goals
                                   if (minimum_diff_for_maccabi <= goal['maccabi_score'] - goal['not_maccabi_score'] <= maximum_diff_for_maccabi)
                                   and goal_condition(goal)]

        important_goals_scorers_names = [goal['name'] for goal in maccabi_important_goals]
        return Counter(important_goals_scorers_names).most_common()

    def get_top_scorers_by_percentage_from_all_their_goals(self, minimum_diff_for_maccabi=-2, maximum_diff_for_maccabi=1, minimum_important_goals=10):
        """
        Return the important goals for each player from his total goals, only for those who scored at least (minimum_important_goals).
        """

        players_total_goals = Counter(dict(self.maccabi_games_stats.players.best_scorers))
        players_important_goals = Counter(dict(self.get_top_scorers(minimum_diff_for_maccabi, maximum_diff_for_maccabi)))

        best_players = Counter()
        for player_name, total_goals_for_player in players_total_goals.items():
            if players_important_goals[player_name] >= minimum_important_goals:
                key_name = "{player} - {total_goals} goals".format(player=player_name, total_goals=total_goals_for_player)
                best_players[key_name] = round(players_important_goals[player_name] / total_goals_for_player * 100, 2)

        return best_players.most_common()

    def get_top_players_for_goals_per_game(self, minimum_diff_for_maccabi=-2, maximum_diff_for_maccabi=1, minimum_games=10):
        """
        Return the important goals for each player from his total goals, only for those who played at least (minimum_games).
        """

        players_total_played = Counter(dict(self.maccabi_games_stats.players.most_played))
        players_important_goals = Counter(dict(self.get_top_scorers(minimum_diff_for_maccabi, maximum_diff_for_maccabi)))

        best_players = Counter()
        for player_name, total_games_for_player in players_total_played.items():
            if players_important_goals[player_name] >= minimum_games:
                key_name = "{player} - {total_games} games".format(player=player_name, total_games=total_games_for_player)
                best_players[key_name] = round(players_important_goals[player_name] / total_games_for_player, 2)

        return best_players.most_common()

    def get_top_scorers_in_last_minutes(self, minimum_diff_for_maccabi=-2, maximum_diff_for_maccabi=1, from_minute=75):
        return self.get_top_scorers(minimum_diff_for_maccabi, maximum_diff_for_maccabi,
                                    lambda g: g['time_occur'] > str(timedelta(minutes=from_minute)))
