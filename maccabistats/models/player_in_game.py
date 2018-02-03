# -*- coding: utf-8 -*-

from maccabistats.models.player_game_events import GameEvent, GameEventTypes
from maccabistats.models.player import Player

from pprint import pformat


class PlayerInGame(Player):
    def __init__(self, name, number, game_events):
        """
        :type name: str.
        :type number: int.
        :type game_events: list of GameEvent
        """

        super(PlayerInGame, self).__init__(name, number)
        self.events = game_events

    def add_event(self, game_event):
        """
        :type game_event: GameEvent
        """

        self.events.append(game_event)

    def has_event_type(self, event_type):
        """"
        :type event_type: GameEventTypes
        :return: bool
        """

        return event_type in [event.event_type for event in self.events]

    def get_events_by_type(self, event_type):
        """
        :type event_type: GameEventTypes
        :rtype: list of GameEvent
        """

        return [event for event in self.events if event.event_type == event_type]

    def event_count_by_type(self, event_type):
        """"
        :type event_type: GameEventTypes
        :rtype: int
        """

        return [event.event_type for event in self.events].count(event_type)

    def goals_count_by_goal_type(self, goal_type):
        """"
        :type goal_type: maccabistats.models.player_game_events.GoalTypes
        :rtype: int
        """

        return [event.goal_type for event in self.get_events_by_type(GameEventTypes.GOAL_SCORE)].count(goal_type)

    def get_as_normal_player(self):
        return Player(self.name, self.number)

    @property
    def played_in_game(self):
        """
        :rtype: bool
        """
        return self.has_event_type(GameEventTypes.LINE_UP) or self.has_event_type(GameEventTypes.SUBSTITUTION_IN)

    @property
    def scored(self):
        """
        :rtype: bool
        """
        return self.has_event_type(GameEventTypes.GOAL_SCORE)

    def get_event_by_similar_event(self, event_to_find):
        """  Return events that equals to the given event.
        :type event_to_find: GameEvent
        :rtype : GameEvent or None
        """

        similar_events = [event for event in self.events if event == event_to_find]
        if len(similar_events) > 1:
            raise Exception("Found 2 events matching this event : {event}".format(event=event_to_find))
        elif not similar_events:
            return None
        else:
            return similar_events[0]

    def __eq__(self, other):
        return self.name == other.name and self.number == other.number

    # In order to save this object in collections.Counter as key
    def __hash__(self):
        return hash((self.name, self.number))

    def __str__(self):
        return super(PlayerInGame, self).__repr__()

    def __repr__(self):
        return "{my_str}" \
               "Player game events: \n{pretty_events}\n\n".format(my_str=self.__str__(),
                                                                  pretty_events=pformat(self.events, indent=4,
                                                                                        width=1))
