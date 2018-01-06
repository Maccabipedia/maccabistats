#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
from maccabi_stats.models.player_in_game import PlayerInGame
from maccabi_stats.models.player_game_events import GameEventTypes


# TODO remove sheran yeini c' in his name (and other captains)

class TeamInGame(object):
    def __init__(self, name, coach, score, players):
        """
        :type name: str.
        :type coach: str.
        :type score: int.
        :type players: list of PlayerInGame
        """

        self.name = name
        self.coach = coach
        self.score = score
        self.players = players

        # In order to get the most common players in each event type, we need to create mapping
        # between event type to the required function, so maccabi wrapper object will know which function to call.
        self.event_type_to_property_of_most_common_players = {
            GameEventTypes.SUBSTITUTION_OUT: self.substitute_off_players_with_amount,
            GameEventTypes.SUBSTITUTION_IN: self.substitute_in_players_with_amount,
            GameEventTypes.GOAL_SCORE: self.scored_players_with_score_amount,
            GameEventTypes.GOAL_ASSIST: self.assist_players_with_score_amount,
            GameEventTypes.LINE_UP: self.lineup_players_with_score_amount,
            GameEventTypes.YELLOW_CARD: self.yellow_carded_players_with_amount,
            GameEventTypes.RED_CARD: self.red_carded_players_with_amount}

    # TODO: add captain as event

    @property
    def lineup_players(self):
        return [player for player in self.players if player.has_event(GameEventTypes.LINE_UP)]

    @property
    def players_from_bench(self):
        return [player for player in self.players if
                player.has_event(GameEventTypes.LINE_UP) and player.has_event(GameEventTypes.SUBSTITUTION_IN)]

    @property
    def not_played_players(self):
        return [player for player in self.players if
                not player.has_event(GameEventTypes.LINE_UP) and not player.has_event(GameEventTypes.SUBSTITUTION_IN)]

    @property
    def scored_players(self):
        return [player for player in self.players if player.has_event(GameEventTypes.GOAL_SCORE)]

    @property
    def assist_players(self):
        return [player for player in self.players if player.has_event(GameEventTypes.GOAL_ASSIST)]

    @property
    def yellow_carded_players(self):
        return [player for player in self.players if player.has_event(GameEventTypes.YELLOW_CARD)]

    @property
    def red_carded_players(self):
        return [player for player in self.players if player.has_event(GameEventTypes.RED_CARD)]

    @property
    def played_players(self):
        return [player for player in self.players if player.played_in_game]

    def __get_players_with_most_of_this_event(self, event_type):
        """
        :type event_type: GameEventTypes
        :rtype: Counter
        """

        return Counter({player: player.event_count(event_type) for player in self.players if
                        player.has_event(event_type)})

    @property
    def scored_players_with_score_amount(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.GOAL_SCORE)

    @property
    def lineup_players_with_score_amount(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.LINE_UP)

    @property
    def assist_players_with_score_amount(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.GOAL_ASSIST)

    @property
    def substitute_off_players_with_amount(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.SUBSTITUTION_OUT)

    @property
    def substitute_in_players_with_amount(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.SUBSTITUTION_IN)

    @property
    def yellow_carded_players_with_amount(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.YELLOW_CARD)

    @property
    def red_carded_players_with_amount(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.RED_CARD)

    @property
    def played_players_with_amount(self):
        """
        :rtype: Counter
        """
        # Return counter of 1 of all played players in game
        return Counter({player: 1 for player in self.played_players})

    def __repr__(self):
        return "Name: {self.name} \n" \
               "Coach: {self.coach}\n" \
               "Players: {self.players}\n\n".format(self=self)
