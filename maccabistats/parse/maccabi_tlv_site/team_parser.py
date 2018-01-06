#!/usr/bin/python
# -*- coding: utf-8 -*-

from maccabistats.models.team_in_game import TeamInGame
from maccabistats.models.player_in_game import PlayerInGame
from maccabistats.models.player_game_events import GameEvent, GameEventTypes

from datetime import timedelta


class MaccabiSiteTeamParser(object):

    @staticmethod
    def parse_team(bs_contents, name, score):
        """
        There are 3 divs for each team ordered as: lineup_players, bench_players, coach.
        :type bs_contents: list of bs4.element.Tag
        :type name: str
        :type score: int
        :rtype : TeamInGame
        """

        players = []
        line_up_players_div = bs_contents[0]

        for line_up_player_bs_content in line_up_players_div.select("li")[1:]:  # Without the first row (Header)
            players.append(MaccabiSiteTeamParser.__parse_player(line_up_player_bs_content, True))

        bench_players_div = bs_contents[1]
        for bench_players_div in bench_players_div.select("li"):
            players.append(MaccabiSiteTeamParser.__parse_player(bench_players_div, False))

        coach = MaccabiSiteTeamParser.__get_coach(bs_contents[2])

        return TeamInGame(name, coach, score, players)

    @staticmethod
    def __parse_player(player_bs_content, is_line_up):
        """
        :type player_bs_content: bs4.element.Tag
        :type is_line_up: bool
        :rtype: PlayerInGame
        """

        player_name = player_bs_content.find(text=True, recursive=False).strip()
        player_number = player_bs_content.find('b').get_text()
        events = []

        if is_line_up:
            events.append(GameEvent(GameEventTypes.LINE_UP, 0))

        for goal_minute in player_bs_content.select_one("div.goals").get_text().split():
            events.append(
                GameEvent(GameEventTypes.GOAL_SCORE, MaccabiSiteTeamParser.__strip_geresh_as_timedelta(goal_minute)))

        MaccabiSiteTeamParser.__append_card_events_for_player(player_bs_content, events)
        MaccabiSiteTeamParser.__append_substitution_events_for_player(player_bs_content, events, is_line_up)

        return PlayerInGame(player_name, player_number, events)

    @staticmethod
    def __append_card_events_for_player(player_bs_content, player_events):
        """
        :type player_bs_content: bs4.element.Tag
        :type player_events: list of GameEvent
        """

        cards_bs_div = [div for div in player_bs_content.select("div") if 'red' in div['id']]

        first_cards_bs_div = cards_bs_div[0]
        card_events_times = first_cards_bs_div.get_text().strip().split()
        if not card_events_times:  # No cards events
            return

        cards_imgs_bs = first_cards_bs_div.find_all("img")
        if len(cards_imgs_bs) != len(card_events_times):  # TODO - delete me - for tests
            print(
                "warning - while parsing cards, cards_Events_times len does not match cards_imgs_bs :{content}".format(
                    content=first_cards_bs_div))
        cards = zip(card_events_times, cards_imgs_bs)

        for card_event_time, card_img_bs in cards:
            card_link = card_img_bs.get("src")
            if card_link.endswith("yellow.png"):
                player_events.append(GameEvent(GameEventTypes.YELLOW_CARD,
                                               MaccabiSiteTeamParser.__strip_geresh_as_timedelta(card_event_time)))
            elif card_link.endswith("red.png"):
                player_events.append(GameEvent(GameEventTypes.RED_CARD,
                                               MaccabiSiteTeamParser.__strip_geresh_as_timedelta(card_event_time)))
            else:
                raise Exception("unknown card {link}".format(link=card_link))

    @staticmethod
    def __append_substitution_events_for_player(player_bs_content, player_events, is_line_up):
        """
        :type player_bs_content: bs4.element.Tag
        :type player_events: list of GameEvent
        :type is_line_up: bool
        """

        substitution_bs_div = [div for div in player_bs_content.select("div") if 'exchange' in div['id']]
        if len(substitution_bs_div) > 1:
            raise Exception("Found 2 substitution divs! - {content}".format(content=substitution_bs_div))

        first_substitution_bs_div = substitution_bs_div[0]
        substitution_events_times = first_substitution_bs_div.get_text().strip().split()
        if not substitution_events_times:  # No substitutions events
            return

        # First Substitution:
        first_substitution_time = substitution_events_times[0]
        if is_line_up:
            player_events.append(GameEvent(GameEventTypes.SUBSTITUTION_OUT,
                                           MaccabiSiteTeamParser.__strip_geresh_as_timedelta(first_substitution_time)))
        else:
            player_events.append(GameEvent(GameEventTypes.SUBSTITUTION_IN,
                                           MaccabiSiteTeamParser.__strip_geresh_as_timedelta(first_substitution_time)))

        # Second Substitution:
        if len(first_substitution_bs_div) == 1:
            return

        # TODO - the lower value from first&seconds substitutions is the subs_in - should check
        second_substitution_time = substitution_events_times[1]
        if is_line_up or len(substitution_events_times) > 2:
            raise Exception("Wrong")
        else:
            player_events.append(GameEvent(GameEventTypes.SUBSTITUTION_OUT,
                                           MaccabiSiteTeamParser.__strip_geresh_as_timedelta(second_substitution_time)))

    @staticmethod
    def __get_coach(bs_content):
        """"
        :type bs_content: bs4.element.Tag
        :rtype: str.
        """

        coach_div_bs = bs_content.select_one("li")
        if coach_div_bs:
            return coach_div_bs.get_text().strip()
        else:
            return "Cant found coach"

    @staticmethod
    def __strip_geresh_as_timedelta(string):
        return timedelta(minutes=int(string.strip().strip("'")))
