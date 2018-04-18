# -*- coding: utf-8 -*-

import logging
import json

from maccabistats.models.player_in_game import PlayerInGame
from maccabistats.models.player_game_events import GameEventTypes
from maccabistats.models.team import Team

from collections import Counter

logger = logging.getLogger(__name__)


class TeamInGame(Team):
    def __init__(self, name, coach, score, players):
        """
        :type name: str.
        :type coach: str.
        :type score: int.
        :type players: list of PlayerInGame
        """

        super(TeamInGame, self).__init__(name)
        self.coach = coach
        self.score = score
        self.players = players

    @property
    def lineup_players(self):
        return [player for player in self.players if player.has_event_type(GameEventTypes.LINE_UP)]

    @property
    def players_from_bench(self):
        return [player for player in self.players if not player.has_event_type(GameEventTypes.LINE_UP) and
                player.has_event_type(GameEventTypes.SUBSTITUTION_IN)]

    @property
    def not_played_players(self):
        return [player for player in self.players if
                not player.has_event_type(GameEventTypes.LINE_UP) and not player.has_event_type(
                    GameEventTypes.SUBSTITUTION_IN)]

    @property
    def scored_players(self):
        return [player for player in self.players if player.has_event_type(GameEventTypes.GOAL_SCORE)]

    @property
    def assist_players(self):
        return [player for player in self.players if player.has_event_type(GameEventTypes.GOAL_ASSIST)]

    @property
    def yellow_carded_players(self):
        return [player for player in self.players if player.has_event_type(GameEventTypes.YELLOW_CARD)]

    @property
    def red_carded_players(self):
        return [player for player in self.players if player.has_event_type(GameEventTypes.RED_CARD)]

    @property
    def played_players(self):
        return [player for player in self.players if player.played_in_game]

    @property
    def captain(self):
        captains = [player for player in self.players if player.has_event_type(GameEventTypes.CAPTAIN)]

        if len(captains) > 1:
            logger.warning("Found {caps} captains, returning the first 1!".format(caps=len(captains)))
            return captains[0]
        elif captains:
            return captains[0]
        else:
            logger.warning("Cant find any captain for this game :(")
            return PlayerInGame("Not a captain", 0, [])

    def get_players_with_most_of_this_condition(self, condition):
        """
        :param condition: this function should get PlayerInGame as param, and return int.
                          0 wont count this player in the final summary.
        :type condition: callable
        :rtype: Counter
        """

        return Counter({player.name: condition(player) for player in self.players if
                        condition(player) > 0})

    @property
    def scored_players_with_score_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_SCORE))

    @property
    def lineup_players_with_score_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.LINE_UP))

    @property
    def assist_players_with_score_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_ASSIST))

    @property
    def substitute_off_players_with_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.SUBSTITUTION_OUT))

    @property
    def substitute_in_players_with_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.SUBSTITUTION_IN))

    @property
    def yellow_carded_players_with_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.YELLOW_CARD))

    @property
    def red_carded_players_with_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.RED_CARD))

    @property
    def captains_players_with_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.CAPTAIN))

    @property
    def penalty_missed_players_with_amount(self):
        return self.get_players_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.PENALTY_MISSED))

    @property
    def played_players_with_amount(self):
        """
        :rtype: Counter
        """
        # Return counter of 1 of all played players in game
        return Counter({player.name : 1 for player in self.played_players})

    def event_type_to_property_of_most_common_players(self, event_type):
        """
        :type event_type: GameEventTypes
        """

        # In order to get the most common players in each event type, we need to create mapping
        # between event type to the required function, so maccabi wrapper object will know which function to call.
        event_type_to_property_of_most_common_players = {
            GameEventTypes.SUBSTITUTION_OUT: self.substitute_off_players_with_amount,
            GameEventTypes.SUBSTITUTION_IN: self.substitute_in_players_with_amount,
            GameEventTypes.GOAL_SCORE: self.scored_players_with_score_amount,
            GameEventTypes.GOAL_ASSIST: self.assist_players_with_score_amount,
            GameEventTypes.LINE_UP: self.lineup_players_with_score_amount,
            GameEventTypes.YELLOW_CARD: self.yellow_carded_players_with_amount,
            GameEventTypes.RED_CARD: self.red_carded_players_with_amount,
            GameEventTypes.CAPTAIN: self.captains_players_with_amount,
            GameEventTypes.PENALTY_MISSED: self.penalty_missed_players_with_amount}

        return event_type_to_property_of_most_common_players[event_type]

    def json_dict(self):
        """
        :rtype: dict
        """
        return dict(name=self.name,
                    score=self.score,
                    coach=self.coach)

    def to_json(self):
        return json.dumps(self.json_dict)

    def __str__(self):
        return "{team_repr}" \
               "Scored: {self.score}\n" \
               "Coach: {self.coach}\n".format(team_repr=super(TeamInGame, self).__repr__(), self=self)

    def __repr__(self):
        return "{my_str}\n" \
               "Players: {self.players}\n\n".format(my_str=self.__str__(), self=self)
