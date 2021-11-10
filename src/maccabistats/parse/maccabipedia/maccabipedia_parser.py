# -*- coding: utf-8 -*-


import logging
from collections import defaultdict
from datetime import timedelta

from dateutil.parser import parse as datetime_parser

from maccabistats.models.game_data import GameData
from maccabistats.models.player_game_events import GameEvent, GameEventTypes, GoalTypes, GoalGameEvent, AssistTypes, \
    AssistGameEvent
from maccabistats.models.player_in_game import PlayerInGame
from maccabistats.models.team_in_game import TeamInGame
from maccabistats.parse.maccabipedia.maccabipedia_cargo_chunks_crawler import MaccabiPediaCargoChunksCrawler

logger = logging.getLogger(__name__)

_PAGE_NAME_FIELD_NAME = "_pageName"
_MACCABI_TEAM = 1
_NOT_MACCABI_TEAM = 0


# MaccabiPedia to Maccabistats event mapping
def _unknown_event():
    return GameEventTypes.UNKNOWN


_EMPTY_SUB_EVENT = ""
_DUPLICATE_MACCABIPEDIA_EVENT = "DUPLICATE"
# If we cant find an event, unknown will be set
MACCABI_PEDIA_EVENTS = defaultdict(_unknown_event,
                                   {1: defaultdict(_unknown_event, {_EMPTY_SUB_EVENT: GameEventTypes.LINE_UP,
                                                                    111: GameEventTypes.LINE_UP}),  # Special for GK
                                    2: defaultdict(_unknown_event, {_EMPTY_SUB_EVENT: GameEventTypes.BENCHED,
                                                                    211: GameEventTypes.BENCHED}),
                                    3: GameEventTypes.GOAL_SCORE,  # Special case, parse also the sub-goal-type
                                    4: GameEventTypes.GOAL_ASSIST,  # Special case, parse also the sub-assist-type

                                    5: defaultdict(_unknown_event, {_EMPTY_SUB_EVENT: GameEventTypes.SUBSTITUTION_IN}),
                                    6: defaultdict(_unknown_event, {_EMPTY_SUB_EVENT: GameEventTypes.SUBSTITUTION_OUT}),
                                    7: defaultdict(_unknown_event, {71: GameEventTypes.YELLOW_CARD,
                                                                    72: GameEventTypes.YELLOW_CARD,
                                                                    73: GameEventTypes.RED_CARD}),
                                    8: defaultdict(_unknown_event, {81: _DUPLICATE_MACCABIPEDIA_EVENT,
                                                                    82: GameEventTypes.PENALTY_MISSED,
                                                                    83: GameEventTypes.PENALTY_STOPPED,
                                                                    84: _DUPLICATE_MACCABIPEDIA_EVENT}),
                                    # No support atm for penalty save
                                    9: defaultdict(_unknown_event, {_EMPTY_SUB_EVENT: GameEventTypes.CAPTAIN})})

MACCABIPEDIA_GOALS_TYPE = {30: GoalTypes.UNCATEGORIZED,
                           31: GoalTypes.NORMAL_KICK,
                           32: GoalTypes.HEADER,
                           33: GoalTypes.OWN_GOAL,
                           34: GoalTypes.FREE_KICK,
                           35: GoalTypes.PENALTY,
                           36: GoalTypes.BICYCLE_KICK,
                           37: GoalTypes.UNKNOWN,
                           }

MACCABIPEDIA_ASSISTS_TYPE = {40: AssistTypes.UNCATEGORIZED,
                             41: AssistTypes.NORMAL_ASSIST,
                             42: AssistTypes.FREE_KICK_ASSIST,
                             43: AssistTypes.CORNER_ASSIST,
                             44: AssistTypes.PENALTY_WINNING_ASSIST,
                             45: AssistTypes.THROW_IN_ASSIST,
                             46: AssistTypes.UNKNOWN,
                             }


class MaccabiPediaParser(object):

    def __init__(self):
        """
        Fetching games table and games_events table from maccabipedia and merge the results (group by the page name)
        """

        # Json as it downloaded from maccabipedia mediawiki api
        self._games_metadata_as_json = self._get_games_metadata()
        self._games_events_as_json = self._get_games_events()

        # Dict from pageName to json
        # TODO: should check if there are more than 1 item in any list, means two game share the same date
        self._game_metadata_by_game = defaultdict(list)
        [self._game_metadata_by_game[game[_PAGE_NAME_FIELD_NAME]].append(game) for game in self._games_metadata_as_json]
        self._games_events_by_game = defaultdict(list)
        [self._games_events_by_game[game_event[_PAGE_NAME_FIELD_NAME]].append(game_event) for game_event in
         self._games_events_as_json]

    @staticmethod
    def _get_games_metadata():
        return [game_metadata_as_json for game_metadata_as_json in
                MaccabiPediaCargoChunksCrawler.create_games_crawler()]

    @staticmethod
    def _get_games_events():
        return [game_events_as_json for game_events_as_json in
                MaccabiPediaCargoChunksCrawler.create_games_events_crawler()]

    def _parse_player_event(self, player_event):
        """
        Parse event from json to maccabistats event format, Maccabipedia contains "double" events (two events for one maccabistats event),
        We ignore those (return None).

        :param player_event: dict

        :rtype: maccabistats.models.player_game_events.GameEvent or None
        """

        event_time = timedelta(minutes=player_event["Minute"])

        if GameEventTypes.GOAL_SCORE == MACCABI_PEDIA_EVENTS[player_event["EventType"]]:
            return GoalGameEvent(time_occur=event_time, goal_type=MACCABIPEDIA_GOALS_TYPE[player_event["SubType"]])
        if GameEventTypes.GOAL_ASSIST == MACCABI_PEDIA_EVENTS[player_event["EventType"]]:
            return AssistGameEvent(time_occur=event_time,
                                   assist_type=MACCABIPEDIA_ASSISTS_TYPE[player_event["SubType"]])
        elif GameEventTypes.UNKNOWN == MACCABI_PEDIA_EVENTS[player_event["EventType"]]:
            return GameEvent(game_event_type=GameEventTypes.UNKNOWN, time_occur=event_time)
        else:
            event_type = MACCABI_PEDIA_EVENTS[player_event["EventType"]][player_event["SubType"]]
            if event_type == GameEventTypes.UNKNOWN:
                logger.warning(f"Encountered unknown event at this event: {player_event}")

            if event_type == _DUPLICATE_MACCABIPEDIA_EVENT:
                return None
            else:
                return GameEvent(game_event_type=event_type, time_occur=event_time)

    def _extract_players_events_for_team(self, game_events_as_json):
        """
        Extract all the players events from the game events.

        :param game_events_as_json: list of game events as json
        :type game_events_as_json: list of dict

        :rtype: list of maccabistats.models.player_in_game.PlayerInGame
        """

        players = []
        # Order all the events by player name:   "PlayerName" to list of his events
        players_events_by_name = defaultdict(list)
        [players_events_by_name[player_event["PlayerName"]].append(player_event) for player_event in
         game_events_as_json]

        for player_name, player_json_events in players_events_by_name.items():
            # Removing any 0 from this player number Set, 0 is a side effect of the events we add on maccabipedia,
            # like penalty scored or missed
            player_number = set(event["PlayerNumber"] for event in player_json_events)

            if len(player_number) > 1:
                non_empty_number = (player_number - {''}) - {0}

                if len(non_empty_number) > 1:
                    logger.warning(f"Found more than 1 player_number for {player_name}: {player_number}, "
                                   f"{player_json_events[0]['_pageName']}")
                else:
                    logger.warning(f"{player_name} has a number in this game: {non_empty_number}, "
                                   f" but at least one event is missing this number,"
                                   f"{player_json_events[0]['_pageName']}")

            player_number = player_number.pop()  # Take the first/only number
            # Adds all events, remove the None ones (means they are duplicates
            player_parsed_events = list(
                filter(None.__ne__, [self._parse_player_event(event) for event in player_json_events]))

            # TODO: handle the case that the number is 0 (no number probably and 0 is because of the db default)
            players.append(PlayerInGame(player_name, player_number, player_parsed_events))

        return players

    def _build_maccabistats_game(self, game_metadata, game_events):
        """
        Build maccabistats game object, creates two teams with their players (and events).

        :param game_metadata: json of the game metadata (coaches names, date and so on)
        :type game_metadata: dict
        :param game_events: players events as json
        :type game_events: list of dict

        :rtype: GameData
        """

        # TODO: atm opponent is number, should add join to the query with opponents table, SAME for competition
        maccabi_players = self._extract_players_events_for_team(
            [event for event in game_events if event['Team'] == _MACCABI_TEAM])
        maccabi_team = TeamInGame("מכבי תל אביב", game_metadata["CoachMaccabi"], game_metadata["ResultMaccabi"],
                                  maccabi_players)

        not_maccabi_players = self._extract_players_events_for_team(
            [event for event in game_events if event['Team'] == _NOT_MACCABI_TEAM])

        not_maccabi_team = TeamInGame(game_metadata["Opponent"], game_metadata["CoachOpponent"],
                                      game_metadata["ResultOpponent"], not_maccabi_players)

        home_team, away_team = (maccabi_team, not_maccabi_team) if game_metadata["HomeAway"] == "בית" else (
            not_maccabi_team, maccabi_team)

        # 'Technical' is 1: for win, 2: for lose, -1: for non technical result game (regular game)
        technical = True if game_metadata['Technical'] in [1, 2] else False

        return GameData(competition=game_metadata["Competition"], fixture=game_metadata["Leg"],
                        date_as_hebrew_string="",
                        stadium=game_metadata["Stadium"], crowd=game_metadata["Crowd"], referee=game_metadata["Refs"],
                        home_team=home_team,
                        away_team=away_team, season_string=str(game_metadata["Season"]), half_parsed_events=[],
                        date=datetime_parser(f"{game_metadata['Date']} {game_metadata['Hour']}"),
                        technical_result=technical)

    def parse(self):
        """
        Building game data from each page name (game metadata & game events).

        :return: List of the merged games from maccabipedia (with the games events)
        :rtype: list of GameData
        """

        parsed_games = []
        for game_name in self._game_metadata_by_game.keys():
            logger.info(f"Parsing game at {game_name}")
            # Take the first game from each date, we should assume its ok or we will have a lot of problems
            parsed_games.append(self._build_maccabistats_game(self._game_metadata_by_game[game_name][0],
                                                              self._games_events_by_game[game_name]))

        return parsed_games
