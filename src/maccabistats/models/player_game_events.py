from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Dict


class AssistTypes(Enum):
    NORMAL_ASSIST = 'NormalAssist'
    FREE_KICK_ASSIST = 'FreeKickAssist'
    CORNER_ASSIST = 'CornerAssist'
    THROW_IN_ASSIST = 'ThrowInAssist'
    PENALTY_WINNING_ASSIST = 'PenaltyWinningAssist'
    UNKNOWN = 'UnknownAssist'


class GoalTypes(Enum):
    FREE_KICK = 'FreeKickGoal'
    PENALTY = 'PenaltyGoal'
    HEADER = 'HeaderGoal'
    OWN_GOAL = 'OwnGoal'
    BICYCLE_KICK = 'BicycleKickGoal'
    NORMAL_KICK = 'NormalGoal'
    UNKNOWN = 'UnknownGoal'

    @classmethod
    def _missing_(cls, value):
        # We use this function in order to allow old MaccabiGamesStats (pickled) to be loaded,
        # We replaced some values, and we want to be able to load this.

        # We can not differentiate between normal and unknown goals in old maccabistats versions
        old_values_mapping = {'normal goal': GoalTypes.UNKNOWN,
                              'Penalty': GoalTypes.PENALTY,
                              'Own goal': GoalTypes.OWN_GOAL,
                              'Free-kick': GoalTypes.FREE_KICK,
                              'Header': GoalTypes.HEADER,
                              'Bicycle-kick': GoalTypes.BICYCLE_KICK}

        if value in old_values_mapping:
            return old_values_mapping[value]

        super()._missing_(value)


class GameEventTypes(Enum):
    GOAL_SCORE = 'ScoreGoal'
    RED_CARD = 'RedCard'
    YELLOW_CARD = 'YellowCard'
    LINE_UP = 'LineUp'
    SUBSTITUTION_IN = 'SubstitutionIn'
    SUBSTITUTION_OUT = 'SubstitutionOut'
    GOAL_ASSIST = 'AssistGoal'
    CAPTAIN = 'Captain'
    PENALTY_MISSED = 'PenaltyMissed'
    PENALTY_STOPPED = 'PenaltyStopped'
    BENCHED = "Benched"
    UNKNOWN = "Unknown"

    @classmethod
    def _missing_(cls, value):
        # We use this function in order to allow old MaccabiGamesStats (pickled) to be loaded,
        # We replaced some values, and we want to be able to load this.
        old_values_mapping = {'Penalty missed': GameEventTypes.PENALTY_MISSED,
                              'Penalty-Missed': GameEventTypes.PENALTY_MISSED,
                              'Line-Up': GameEventTypes.LINE_UP,
                              'Score-Goal': GameEventTypes.GOAL_SCORE,
                              'Assist-Goal': GameEventTypes.GOAL_ASSIST,
                              'Substitution-In': GameEventTypes.SUBSTITUTION_IN,
                              'Substitution-Out': GameEventTypes.SUBSTITUTION_OUT,
                              'Red-Card': GameEventTypes.RED_CARD,
                              'Yellow-Card': GameEventTypes.YELLOW_CARD,
                              'Penalty-Stopped': GameEventTypes.PENALTY_STOPPED}

        if value in old_values_mapping:
            return old_values_mapping[value]

        super()._missing_(value)


@dataclass(repr=False)
class GameEvent:
    event_type: GameEventTypes
    time_occur: timedelta

    def __repr__(self) -> str:
        extra_repr_info = self._extra_repr_info()
        extra_repr_info = f' ({extra_repr_info})' if extra_repr_info else extra_repr_info

        return f"{self.event_type.value} at {self.time_occur}{extra_repr_info}"

    def _extra_repr_info(self) -> str:
        return ''

    def json_dict(self) -> Dict:
        return dict(event_type=self.event_type.value,
                    time_occur=str(self.time_occur))


@dataclass(repr=False)
class GoalGameEvent(GameEvent):
    goal_type: GoalTypes = GoalTypes.UNKNOWN

    def _extra_repr_info(self) -> str:
        return f'type: {self.goal_type.value}'

    def json_dict(self) -> Dict:
        base_class_json_dict = super().json_dict()

        base_class_json_dict['goal_type'] = self.goal_type.value
        return base_class_json_dict


@dataclass(repr=False)
class AssistGameEvent(GameEvent):
    assist_type: AssistTypes = AssistTypes.UNKNOWN

    def _extra_repr_info(self) -> str:
        return f'type: {self.assist_type.value}'

    def json_dict(self) -> Dict:
        base_class_json_dict = super().json_dict()

        base_class_json_dict['assist_type'] = self.assist_type.value
        return base_class_json_dict
