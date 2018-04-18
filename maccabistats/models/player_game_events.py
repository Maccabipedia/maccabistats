# -*- coding: utf-8 -*-

from enum import Enum
from datetime import timedelta


class GoalTypes(Enum):
    FREE_KICK = 'Free-kick'
    PENALTY = 'Penalty'
    HEADER = 'Header'
    OWN_GOAL = 'Own goal'
    UNKNOWN = 'normal goal'


class GameEventTypes(Enum):
    GOAL_SCORE = 'Score-Goal'
    RED_CARD = 'Red-Card'
    YELLOW_CARD = 'Yellow-Card'
    LINE_UP = 'Line-Up'
    SUBSTITUTION_IN = 'Substitution-In'
    SUBSTITUTION_OUT = 'Substitution-Out'
    GOAL_ASSIST = 'Assist-Goal'
    CAPTAIN = 'Captain'
    PENALTY_MISSED = 'Penalty missed'
    BENCHED = "Benched"


class GameEvent(object):
    def __init__(self, game_event_type, time_occur):
        """
        :type game_event_type: GameEventTypes
        :type time_occur: timedelta
        """
        self.event_type = game_event_type

        if type(time_occur) is not timedelta:
            raise Exception("not timedelta")
        self.time_occur = time_occur

    def __repr__(self):
        return "{self.event_type.value} occur at {self.time_occur}".format(self=self)

    def __eq__(self, other):
        """
        :type other: GameEvent
        :return: bool
        """
        return self.event_type == other.event_type and self.time_occur == other.time_occur

    def json_dict(self):
        """
        :rtype: dict
        """
        return dict(event_type=self.event_type.value,
                    time_occur=str(self.time_occur))


class GoalGameEvent(GameEvent):
    def __init__(self, time_occur, goal_type=GoalTypes.UNKNOWN):
        """
        :type time_occur: timedelta
        :type goal_type: GoalTypes
        """

        super(GoalGameEvent, self).__init__(GameEventTypes.GOAL_SCORE, time_occur)
        self.goal_type = goal_type

    def __repr__(self):
        return "{game_event}\n" \
               "Goal type : {self.goal_type}".format(game_event=super(GoalGameEvent, self).__repr__(), self=self)

    def json_dict(self):
        """
        :rtype: dict
        """
        base_class_json_dict = super(GoalGameEvent, self).json_dict()
        base_class_json_dict['goal_type'] = self.goal_type.value
        return base_class_json_dict
