# -*- coding: utf-8 -*-

from functools import reduce
from collections import Counter

from maccabistats.models.player_game_events import GameEventTypes, GoalTypes


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
             for game in self.games])

        # Remove the events by cast player_in_game to 'player' object
        return Counter(
            {player_in_game.get_as_normal_player(): players_with_most_event_type[player_in_game] for player_in_game
             in
             players_with_most_event_type}).most_common()

    @property
    def best_scorers(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_SCORE))

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
    def most_played(self):
        """
        :rtype: Counter
        """
        # Like __get_players_with_most_of_this_event
        most_played_players = reduce(
            lambda played_counter_a, played_counter_b: played_counter_a + played_counter_b,
            [game.maccabi_team.played_players_with_amount
             for game in self.games])

        # Remove the events by cast player_in_game to 'player' object
        return Counter(
            {player_in_game.get_as_normal_player(): most_played_players[player_in_game] for player_in_game
             in
             most_played_players}).most_common()
