from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional, cast

from maccabistats.models.player import Player
from maccabistats.models.player_game_events import GameEvent, GameEventTypes, GoalTypes, GoalGameEvent


@dataclass
class PlayerInGame(Player):
    events: List[GameEvent]

    def add_event(self, game_event: GameEvent) -> None:
        self.events.append(game_event)

    def has_event_type(self, event_type: GameEventTypes) -> bool:
        # TODO: might use any
        return event_type in [event.event_type for event in self.events]

    def get_events_by_type(self, event_type: GameEventTypes) -> List[GameEvent]:
        return [event for event in self.events if event.event_type == event_type]

    def event_count_by_type(self, event_type: GameEventTypes) -> int:
        # TODO: create temp list with only the required event type and check the len of it ( O(1) )
        return [event.event_type for event in self.events].count(event_type)

    def goals_count_by_goal_type(self, goal_type: GoalTypes) -> int:
        return [cast(GoalGameEvent, event).goal_type for event in
                self.get_events_by_type(GameEventTypes.GOAL_SCORE)].count(goal_type)

    def get_as_normal_player(self) -> Player:
        return Player(self.name, self.number)

    @property
    def played_in_game(self) -> bool:
        return self.has_event_type(GameEventTypes.LINE_UP) or self.has_event_type(GameEventTypes.SUBSTITUTION_IN)

    @property
    def scored(self) -> bool:
        return self.has_event_type(GameEventTypes.GOAL_SCORE)

    @property
    def scored_after_sub_in(self) -> bool:
        """
        Whether this players scored after a sub in
        """
        if not self.scored:
            return False

        min_goal_time = min(goal.time_occur for goal in self.get_events_by_type(GameEventTypes.GOAL_SCORE))
        subs_in_time = self.get_events_by_type(GameEventTypes.SUBSTITUTION_IN)[0].time_occur

        # Avoid bugs in maccabi site which registered players as subs in min 0.
        if subs_in_time == timedelta(seconds=0):
            return False

        return min_goal_time >= subs_in_time

    def get_event_by_similar_event(self, event_to_find: GameEvent) -> Optional[GameEvent]:
        """  Return events that equals to the given event.
        :type event_to_find: GameEvent
        """
        similar_events = [event for event in self.events if event == event_to_find]
        if len(similar_events) > 1:
            raise Exception("Found 2 events matching this event : {event}".format(event=event_to_find))
        elif not similar_events:
            return None
        else:
            return similar_events[0]
