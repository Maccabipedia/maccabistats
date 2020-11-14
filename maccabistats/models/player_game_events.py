from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Dict


class GoalTypes(Enum):
    FREE_KICK = 'Free-kick'
    PENALTY = 'Penalty'
    HEADER = 'Header'
    OWN_GOAL = 'Own goal'
    UNKNOWN = 'normal goal'
    BICYCLE_KICK = 'Bicycle-kick'


class GameEventTypes(Enum):
    GOAL_SCORE = 'Score-Goal'
    RED_CARD = 'Red-Card'
    YELLOW_CARD = 'Yellow-Card'
    LINE_UP = 'Line-Up'
    SUBSTITUTION_IN = 'Substitution-In'
    SUBSTITUTION_OUT = 'Substitution-Out'
    GOAL_ASSIST = 'Assist-Goal'
    CAPTAIN = 'Captain'
    PENALTY_MISSED = 'Penalty-Missed'
    PENALTY_STOPPED = 'Penalty-Stopped'
    BENCHED = "Benched"
    UNKNOWN = "Unknown"


class GameEvent(object):
    def __init__(self, game_event_type: GameEventTypes, time_occur: timedelta):
        self.event_type = game_event_type

        if not isinstance(time_occur, timedelta):
            raise Exception(f"time_occur parameter should be instance of timedelta: {time_occur}")

        self.time_occur = time_occur

    def __repr__(self) -> str:
        return "{self.event_type.value} occur at {self.time_occur}".format(self=self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameEvent):
            return NotImplemented

        return self.event_type == other.event_type and self.time_occur == other.time_occur

    def json_dict(self) -> Dict:
        return dict(event_type=self.event_type.value,
                    time_occur=str(self.time_occur))


class GoalGameEvent(GameEvent):
    def __init__(self, time_occur: timedelta, goal_type: GoalTypes = GoalTypes.UNKNOWN):

        super(GoalGameEvent, self).__init__(GameEventTypes.GOAL_SCORE, time_occur)
        self.goal_type = goal_type

    def __repr__(self) -> str:
        return "{game_event}\n" \
               "Goal type : {self.goal_type}".format(game_event=super(GoalGameEvent, self).__repr__(), self=self)

    def json_dict(self) -> Dict:
        base_class_json_dict = super(GoalGameEvent, self).json_dict()

        base_class_json_dict['goal_type'] = self.goal_type.value
        return base_class_json_dict
