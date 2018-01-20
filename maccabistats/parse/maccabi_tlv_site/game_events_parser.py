# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import timedelta
import logging

from maccabistats.models.player_game_events import GameEventTypes, GoalGameEvent, GameEvent, GoalTypes

logger = logging.getLogger(__name__)
fully_game_time_without_penalties = timedelta(minutes=120)


class CantFindEventException(Exception):
    pass


class ComplicatedEventException(Exception):
    pass


class MaccabiSiteGameEventsParser(object):

    def __init__(self, maccabi_team, not_maccabi_team, bs_content):
        """
        There are 3 divs for each team ordered as: lineup_players, bench_players, coach.
        :type bs_content: bs4.element.Tag
        :type maccabi_team: maccabistats.models.team_in_game.TeamInGame
        :type not_maccabi_team: maccabistats.models.team_in_game.TeamInGame
        """

        self.bs_content = bs_content
        self.maccabi_team = maccabi_team
        self.not_maccabi_team = not_maccabi_team
        self.events_bs_content_list = self.bs_content.select("article div.play-by-play-homepage ul.play-by-play li")

        # TODO - this should be oneliner
        self.event_type_to_handler_function = defaultdict(self.__handle_unknown_event)
        self.event_type_to_handler_function["red"] = self.__handle_red_card_event
        self.event_type_to_handler_function["yellow"] = self.__handle_yellow_card_event
        self.event_type_to_handler_function["assist"] = self.__handle_assist_event
        self.event_type_to_handler_function["goal"] = self.__handle_goal_event
        self.event_type_to_handler_function["sub"] = self.__handle_substitution_event
        self.event_type_to_handler_function["penalty-missed"] = self.__handle_penalty_missed_event
        self.event_type_to_handler_function["secondyellow"] = self.__handle_second_yellow_card_missed_event
        self.event_type_to_handler_function["whistle"] = self.__handle_ignored_events

    def enrich_teams_with_events(self):
        """ Return the enriched (with game events) teams.
        :rtype: TeamInGame, TeamInGame
        """

        for event_id, event_bs_content in enumerate(self.events_bs_content_list):
            event_time_in_minute = timedelta(minutes=int(event_bs_content.select_one("div.min").get_text()))
            event_type = event_bs_content['class'][0]
            event_text = event_bs_content.select_one("p").get_text().strip()

            if fully_game_time_without_penalties <= event_time_in_minute:
                logger.info("Ignoring event in minute {min}".format(min=event_time_in_minute.seconds/60.0))
                continue
            try:
                # should be like - defaultdict seems to call the default function when just trying to access the key:
                # self.event_type_to_handler_function[event_type](event_bs_content, event_text, event_time_in_minute)
                if event_type in self.event_type_to_handler_function:
                    self.event_type_to_handler_function[event_type](event_text, event_time_in_minute)
                else:
                    self.__handle_unknown_event(event_bs_content, event_text, event_time_in_minute)
            except ComplicatedEventException as e:
                logger.info("ComplicatedEventException : {details}".format(details=str(e)))
            except CantFindEventException as e:
                logger.exception("CantFindEventException : {details}".format(details=str(e)))
            except Exception as e:
                logger.exception(str(e))

        return self.maccabi_team, self.not_maccabi_team

    def __find_one_player_with_name(self, player_name):
        """ Finds player by his name, validate that only 1 player have been found

        :rtype : PlayerInGame
        """

        player_name = player_name.replace("\u202a", "").replace("\u200f", "").strip()

        if len(player_name) > 20:
            raise ComplicatedEventException(player_name)

        players = [player for player in self.maccabi_team.players if player.name == player_name]
        players.extend([player for player in self.not_maccabi_team.players if player.name == player_name])

        if len(players) > 1:
            logger.warning("Found more than 1 player named :{player_name}".format(player_name=player_name))
        elif len(players) == 0:
            raise Exception("Game link : {link}\n"
                            "Cant find player with that name : {name}".format(link=self.maccabi_team.game_link,
                                                                              name=player_name))

        return players[0]

    def __get_player_event(self, player, event):
        """ Check whether the given player got event in specific time
        :type player: maccabistats.models.player_in_game.PlayerInGame
        :type event: maccabistats.models.player_game_events.GameEvent
        :rtype: maccabistats.models.player_game_events.GameEvent
        """

        player_event = player.get_event_by_similar_event(event)

        if not player_event:
            logger.warning("Game link : {link}\n"
                           "Found event : {event}\n"
                           "Which this player supposed to have: {player}".format(link=self.maccabi_team.game_link,
                                                                                 event=event, player=player))
            raise CantFindEventException("cant find event : {event}".format(event=event))

        return player_event

    def __handle_ignored_events(self, event_text, event_time_in_minute):
        pass

    def __handle_penalty_missed_event(self, event_text, event_time_in_minute):
        player_name = event_text.replace("פנדל הוחמץ על ידי", "").strip()
        player = self.__find_one_player_with_name(player_name)

        penalty_missed = GameEvent(GameEventTypes.PENALTY_MISSED, event_time_in_minute)
        player.add_event(penalty_missed)
        logger.info(
            "Added penalty missed for player: {player}".format(player=player_name))

    def __handle_second_yellow_card_missed_event(self, event_text, event_time_in_minute):
        player_name = event_text.replace("כרטיס צהוב שני ל", "").strip()
        player = self.__find_one_player_with_name(player_name)

        # TODO - do we need second yellow event?
        yellow_event = GameEvent(GameEventTypes.YELLOW_CARD, event_time_in_minute)
        try:
            player_event = self.__get_player_event(player, yellow_event)
            logger.info("Found second yellow event : {event}".format(event=player_event))
        except CantFindEventException:
            player.add_event(yellow_event)
            logger.info("Added second yellow event for player: {player}".format(player=player_name))

    def __handle_substitution_event(self, event_text, event_time_in_minute):
        player_name_sub_in, player_name_sub_out = event_text.strip().split("החליף את")
        player_sub_in = self.__find_one_player_with_name(player_name_sub_in)
        player_sub_out = self.__find_one_player_with_name(player_name_sub_out)

        sub_in_event = GameEvent(GameEventTypes.SUBSTITUTION_IN, event_time_in_minute)
        sub_out_event = GameEvent(GameEventTypes.SUBSTITUTION_OUT, event_time_in_minute)

        try:
            self.__get_player_event(player_sub_in, sub_in_event)
            logger.info("Found subs in event: {event}".format(event=sub_in_event))
        except CantFindEventException:
            player_sub_in.add_event(sub_in_event)
            logger.info("Added subs-in event for player: {player}".format(player=player_name_sub_in))

        try:
            self.__get_player_event(player_sub_out, sub_out_event)
            logger.info("Found subs out event: {event}".format(event=sub_out_event))
        except CantFindEventException:
            player_sub_in.add_event(sub_in_event)
            logger.info("Added subs-out event for player: {player}".format(player=player_name_sub_out))

    @staticmethod
    def __extract_goal_details(event_text, event_time_in_minute):
        """ Extracting final player name from the event_Text + creating goal event.
        :rtype: str, GoalGameEvent
        """

        player_name = event_text.replace("שער של", "").strip()
        goal_type = GoalTypes.UNKNOWN

        if "(פנדל)" in player_name:
            player_name = player_name.replace("(פנדל)", "").strip()
            goal_type = GoalTypes.PENALTY

        elif "פנדל הובקע על ידי" in player_name:
            player_name = player_name.replace("פנדל הובקע על ידי", "").strip()
            goal_type = GoalTypes.PENALTY

        elif "(שער עצמי)" in player_name:
            player_name = player_name.replace("(שער עצמי)", "").strip()
            goal_type = GoalTypes.OWN_GOAL

        goal_event = GoalGameEvent(event_time_in_minute, goal_type)

        return player_name, goal_event

    def __handle_goal_event(self, event_text, event_time_in_minute):
        player_name, goal_event = MaccabiSiteGameEventsParser.__extract_goal_details(event_text, event_time_in_minute)

        player = self.__find_one_player_with_name(player_name)
        player_event = self.__get_player_event(player, goal_event)

        # Add goal type:
        if goal_event.goal_type is not GoalTypes.UNKNOWN:
            player_event.goal_type = goal_event.goal_type
            logger.info(
                "Changed goal type to {goal_type} for player: {player}".format(goal_type=goal_event.goal_type,
                                                                               player=player.name))

    def __handle_yellow_card_event(self, event_text, event_time_in_minute):
        player_name = event_text.replace("כרטיס צהוב ל", "").strip()
        player = self.__find_one_player_with_name(player_name)

        yellow_card_event = GameEvent(GameEventTypes.YELLOW_CARD, event_time_in_minute)

        self.__get_player_event(player, yellow_card_event)

    def __handle_red_card_event(self, event_text, event_time_in_minute):
        player_name = event_text.replace("כרטיס אדום ל", "").strip()
        player = self.__find_one_player_with_name(player_name)

        red_card_event = GameEvent(GameEventTypes.RED_CARD, event_time_in_minute)
        try:
            player_event = self.__get_player_event(player, red_card_event)
            logger.info("Found red card event : {event}".format(event=player_event))
        except CantFindEventException:
            player.add_event(red_card_event)
            logger.info("Added red card event for player: {player}".format(player=player.name))

    def __handle_assist_event(self, event_text, event_time_in_minute):
        player_name = event_text.replace("בישול על ידי", "").strip()
        player = self.__find_one_player_with_name(player_name)

        assist_event = GameEvent(GameEventTypes.GOAL_ASSIST, event_time_in_minute)
        player.add_event(assist_event)
        logger.info("Added assist event for player: {player}".format(player=player_name))

    @staticmethod
    def __handle_unknown_event(event_bs_content, event_text, event_time_in_minute):
        event_type = event_bs_content['class'][0]
        logger.info("Unknown event type :{event_type} in minute :{minute}\n"
                    "With event text :{event_text}".format(event_type=event_type,
                                                           minute=event_time_in_minute, event_text=event_text))
