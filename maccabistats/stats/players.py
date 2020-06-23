# -*- coding: utf-8 -*-


from collections import Counter
from datetime import timedelta
from functools import reduce
import logging
from maccabistats.models.player_game_events import GameEventTypes, GoalTypes


logger = logging.getLogger(__name__)
# This class will handle all players statistics.


class MaccabiGamesPlayersStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.games = maccabi_games_stats.games

    def __get_players_from_all_games_with_most_of_this_condition(self, condition):
        """
        :param condition: this function should get PlayerInGame as param, and return int.
                          0 wont count this player in the final summary.
        :type condition: callable
        :rtype: Counter
        """
        players_with_most_event_type = reduce(
            lambda events_counter_a, events_counter_b: events_counter_a + events_counter_b,

            # TeamInGame saves dict which map between player event to the property
            # which return the most common players which have this event in this game & team.
            [game.maccabi_team.get_players_with_most_of_this_condition(condition)
             for game in self.games],
            Counter([]))  # When self.games above is empty, reduce will return this default value.

        return players_with_most_event_type.most_common()

    def get_top_scorers_on_last_minutes(self, from_minute=75):
        from_this_minute_str = str(timedelta(minutes=from_minute))
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: len([event for event in p.events
                           if event.event_type == GameEventTypes.GOAL_SCORE and str(event.time_occur) > from_this_minute_str]))

    def get_top_players_for_goals_per_game(self, minimum_games_played=10):
        players_total_played = Counter(dict(self.most_played))
        players_total_goals = Counter(dict(self.best_scorers))

        best_players = Counter()
        for player_name, total_games_for_player in players_total_played.items():
            if total_games_for_player >= minimum_games_played:
                key_name = "{player} - {total_games} games".format(player=player_name, total_games=total_games_for_player)
                best_players[key_name] = round(players_total_goals[player_name] / total_games_for_player, 2)

        return best_players.most_common()

    @property
    def best_scorers(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_SCORE) - p.goals_count_by_goal_type(GoalTypes.OWN_GOAL))

    @property
    def best_scorers_by_freekick(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.FREE_KICK))

    @property
    def best_scorers_by_penalty(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.PENALTY))

    @property
    def best_scorers_by_head(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.HEADER))

    @property
    def best_scorers_by_own_goal(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.OWN_GOAL))

    @property
    def best_assisters(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_ASSIST))

    @property
    def most_goals_involved(self):
        """
        Top players which involved in goals (score or assist)
        """

        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_ASSIST) + p.event_count_by_type(
                GameEventTypes.GOAL_SCORE) - p.goals_count_by_goal_type(GoalTypes.OWN_GOAL))

    @property
    def most_yellow_carded(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.YELLOW_CARD))

    @property
    def most_red_carded(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.RED_CARD))

    @property
    def most_substitute_off(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.SUBSTITUTION_OUT))

    @property
    def most_substitute_in(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.SUBSTITUTION_IN))

    @property
    def most_lineup_players(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.LINE_UP))

    @property
    def most_captains(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.CAPTAIN))

    @property
    def most_penalty_missed(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.PENALTY_MISSED))

    @property
    def most_penalty_stopped(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.PENALTY_STOPPED))

    def __get_players_with_most_of_this_game_condition(self, condition=None):
        """
        Return the players which played the most at games with the given condition,
        example: __get_players_with_most_of_this_game_condition(lambda g: g.is_maccabi_win)
        for players who played when maccabi won.
        :param condition: callable which get game as param and return bool (if need to count this game).
        :type condition: callable(maccabistats.models.game_data.GameData) -> bool
        """

        if condition is None:
            condition = lambda g: True

        # Like __get_players_with_most_of_this_event
        most_played_players_with_game_condition = reduce(
            lambda played_counter_a, played_counter_b: played_counter_a + played_counter_b,
            [game.maccabi_team.played_players_with_amount
             for game in self.games if condition(game)])

        return Counter(most_played_players_with_game_condition).most_common()

    @property
    def most_winners(self):
        """
        Return the players who played at most when maccabi won.
        """

        return self.__get_players_with_most_of_this_game_condition(lambda g: g.is_maccabi_win)

    @property
    def most_losers(self):
        """
        Return the players who played at most when maccabi lost.
        """

        return self.__get_players_with_most_of_this_game_condition(lambda g: g.maccabi_score_diff < 0)

    @property
    def most_unbeaten(self):
        """
        Return the players who played at most when maccabi not lost.
        """

        return self.__get_players_with_most_of_this_game_condition(lambda g: g.maccabi_score_diff >= 0)

    @property
    def most_clean_sheet(self):
        """
        Return the players who played at most when maccabi had no goals scored against her.
        """

        return self.__get_players_with_most_of_this_game_condition(lambda g: g.not_maccabi_team.score == 0)

    @property
    def most_played(self):
        """
        :rtype: Counter
        """

        return self.__get_players_with_most_of_this_game_condition(lambda g: True)

    @staticmethod
    def __goals_count_after_sub_in(player):
        """
        Count the goals after sub in for this player
        :type player: maccabistats.models.player_in_game.PlayerInGame
        :rtype: int
        """
        if not player.scored:
            return 0
        if not player.has_event_type(GameEventTypes.SUBSTITUTION_IN):
            return 0

        count_by_goals = player.event_count_by_type(GameEventTypes.GOAL_SCORE)

        subs_in_time = player.get_events_by_type(GameEventTypes.SUBSTITUTION_IN)[0].time_occur
        count_goals_after_sub = len([goal for goal in player.get_events_by_type(GameEventTypes.GOAL_SCORE) if goal.time_occur >= subs_in_time])

        # Avoid bugs in maccabi site which registered players as subs in min 0.
        if subs_in_time == timedelta(seconds=0):
            return False

        if count_by_goals != count_goals_after_sub:
            # TODO: This is just for safety
            logger.error(f"A player: {player.name} has different number of goals in 'goals_after_sub_in' calculation.")

            return 0

        return count_by_goals

    @property
    def most_goals_after_sub_in(self):
        """
        :rtype: Counter
        """
        return self.__get_players_from_all_games_with_most_of_this_condition(lambda p: self.__goals_count_after_sub_in(p))

    def __get_most_players_by_percentage_with_this_game_condition(self, players_ordered_by_game_condition,
                                                                  minimum_games_played=0):
        """
        Return list of players ordered by their percentage of (played games with this condition) / (played games)
        example : __get_most_players_by_percentage_with_this_game_condition(self.most_winner)
        for list of most winner players by percentage.
        Filter can be done with minimum_games_played to ignore players with high percentage and few games played.
        :param players_ordered_by_game_condition: Dict of players ordered by game condition,
                                                  dict key: player(normal player - without events)
                                                  dict value: count of game the player played with the game condition.
        :type players_ordered_by_game_condition: dict from maccabistats.model.player_in_game.PlayerInGame to int
        :param minimum_games_played: used to ignore players with high percentage and few games.
        :type minimum_games_played: int
        """

        total_players_games = dict(self.most_played)

        players_percentage = [dict(name=player,
                                   percentage=round(
                                       players_ordered_by_game_condition.get(player, 0) * 100 /  # 100 for percentage
                                       total_players_games[player], 3),
                                   total_games=total_players_games[player])

                              for player in total_players_games.keys()
                              if total_players_games[player] >= minimum_games_played]

        sorted_players_percentage = sorted(players_percentage, key=lambda w: w['percentage'], reverse=True)
        return sorted_players_percentage

    def get_most_winners_by_percentage(self, minimum_games_played=0):
        """
        Returns sorted list of (player, wins, played) for each player.

        :param minimum_games_played: minimum games player have been played to be included in the list.
        :rtype: list of dict
        """

        return self.__get_most_players_by_percentage_with_this_game_condition(dict(self.most_winners),
                                                                              minimum_games_played)

    def get_most_losers_by_percentage(self, minimum_games_played=0):
        """
        Returns sorted list of (player, losses, played) for each player.

        :param minimum_games_played: minimum games player have been played to be included in the list.
        :rtype: list of dict
        """

        return self.__get_most_players_by_percentage_with_this_game_condition(dict(self.most_losers),
                                                                              minimum_games_played)

    def get_most_unbeaten_by_percentage(self, minimum_games_played=0):
        """
        Returns sorted list of (player, unbeaten, played) for each player.

        :param minimum_games_played: minimum games player have been played to be included in the list.
        :rtype: list of dict
        """

        return self.__get_most_players_by_percentage_with_this_game_condition(dict(self.most_unbeaten),
                                                                              minimum_games_played)

    def get_most_clean_sheet_by_percentage(self, minimum_games_played=0):
        """
        Returns sorted list of (player, clean_sheer, played) for each player.

        :param minimum_games_played: minimum games player have been played to be included in the list.
        :rtype: list of dict
        """

        return self.__get_most_players_by_percentage_with_this_game_condition(dict(self.most_clean_sheet),
                                                                              minimum_games_played)
