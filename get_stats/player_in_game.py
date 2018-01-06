#!/usr/bin/python
# -*- coding: utf-8 -*-

from get_stats.player_game_events import GameEvent, GameEventTypes
from get_stats.player import Player

from pprint import pformat


class PlayerInGame(Player):
    def __init__(self, name, number, game_events):
        """
        :type name: str.
        :type number: int.
        :type game_events: list of GameEvent
        """
        # TODO : check if should call to super first or after self assign
        super(PlayerInGame, self).__init__(name, number)
        self.events = game_events

    def add_event(self, game_event):
        """
        :type game_event: GameEvent
        """

        self.events.append(game_event)

    def has_event(self, event_type):
        """"
        :type event_type: GameEventTypes
        :return: bool
        """

        return event_type in [event.event_type for event in self.events]

    def event_count(self, event_type):
        """"
        :type event_type: GameEventTypes
        :return: int
        """

        return [event.event_type for event in self.events].count(event_type)

    def get_as_normal_player(self):
        return Player(self.name, self.number)


    @property
    def played_in_game(self):
        """
        :rtype: bool
        """
        return self.has_event(GameEventTypes.LINE_UP) or self.has_event(GameEventTypes.SUBSTITUTION_IN)

    def __eq__(self, other):
        return self.name == other.name and self.number == other.number

    def __hash__(self):
        return hash((self.name, self.number))

    def __repr__(self):
        return "{player_repr}" \
               "Player game events: \n{pretty_events}\n\n".format(player_repr=super(PlayerInGame, self).__repr__(),
                                                                  pretty_events=pformat(self.events, indent=4,
                                                                                        width=1))
