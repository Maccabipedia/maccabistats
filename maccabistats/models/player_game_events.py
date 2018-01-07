#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum
from datetime import timedelta


class GameEventTypes(Enum):
    # TODO - we should had the type of goal - free-kick, by head, penalty kick and so on
    GOAL_SCORE = 'Score-Goal'
    RED_CARD = 'Red-Card'
    YELLOW_CARD = 'Yellow-Card'
    LINE_UP = 'Line-Up'
    SUBSTITUTION_IN = 'Substitution-In'
    SUBSTITUTION_OUT = 'Substitution-Out'
    GOAL_ASSIST = 'Assist-Goal'
    CAPTAIN = 'Captain'


class GameEvent(object):
    def __init__(self, game_event_type, time_occur):
        """
        :type game_event_type: GameEventTypes
        :type time_occur: timedelta or float or int
        """
        self.event_type = game_event_type
        self.time_occur = time_occur

    def __repr__(self):
        return "{self.event_type.value} occur at {self.time_occur}".format(self=self)
