#!/usr/bin/python
# -*- coding: utf-8 -*-


from maccabi_stats.models.game_data import GameData
from maccabi_stats.parse.maccabi_tlv_site.team_parser import MaccabiSiteTeamParser
from maccabi_stats.parse.maccabi_tlv_site.games_from_maccabi_site import get_game_squads_bs_by_link

from urllib.parse import unquote


class MaccabiSiteGameParser(object):

    @staticmethod
    def parse_game(bs_content):
        """
        Gets an html content which relevant to maccabi game and return GameData object, uses bs4.BeautifulSoup.

        :param bs_content: the part of the html, like soup.find("article"), where soup is BeautifulSoup object.
        :type bs_content: bs4.element.Tag
        :return: GameData
        """

        competition = bs_content.find("div", "league-title").get_text()
        fixture = MaccabiSiteGameParser.__get_fixture_if_exists(bs_content, competition)

        date = MaccabiSiteGameParser.__get_full_date(bs_content)
        stadium = bs_content.select_one("div.location div").get_text().split(" ", 1)[1]

        maccabi_final_score = int(bs_content.select_one("span.ss.maccabi.h").get_text())
        # Looking for <span class="ss h"> for not maccabi score
        not_maccabi_final_score = int([span.get_text() for span in bs_content.select("span.ss.h")
                                       if 'maccabi' not in span.attrs['class']][0])

        maccabi_team_name = "מכבי תל אביב"
        not_maccabi_team_name = bs_content.select_one("div.holder.notmaccabi.nn").get_text()

        maccabi_is_home_team = bs_content.select_one("div.matchresult.Home") is not None

        game_content_web_page = unquote(bs_content.find("a", href=True).get("href"))
        squads_bs_page_content = get_game_squads_bs_by_link(game_content_web_page)
        # TODO: move this to another static method -> save_game_web_page_to_disk(self.game_content_web_page)

        maccabi_team, not_maccabi_team = MaccabiSiteGameParser.__get_teams(squads_bs_page_content,
                                                                           maccabi_team_name,
                                                                           not_maccabi_team_name,
                                                                           maccabi_final_score,
                                                                           not_maccabi_final_score)
        referee = MaccabiSiteGameParser.__get_referee(squads_bs_page_content)
        crowd = MaccabiSiteGameParser.__get_crowd(squads_bs_page_content)

        home_team, away_team = (maccabi_team, not_maccabi_team) if maccabi_is_home_team else (
            not_maccabi_team, maccabi_team)

        return GameData(competition, fixture, date, stadium, crowd, referee, home_team, away_team, maccabi_is_home_team)

    @staticmethod
    def __get_fixture_if_exists(bs_content, competition):
        """
        :type bs_content: bs4.element.Tag
        :return: str
        """

        fixture_div = bs_content.find("div", "round")
        if fixture_div:
            return fixture_div.get_text()
        else:
            print("Cant found round for {competition}".format(competition=competition))
            return "No round found"

    @staticmethod
    def __get_full_date(bs_content):
        """
        :type bs_content: bs4.element.Tag
        :return: str
        """
        date_without_hour = bs_content.select_one("div.location span").get_text()
        date_hour = bs_content.select_one("div.location div").get_text().split(" ", 1)[0]
        return " ".join([date_without_hour, date_hour])

    @staticmethod
    def __get_teams(bs_content, maccabi_team_name, not_maccabi_team_name, maccabi_score, not_maccabi_score):
        """
        :type bs_content: bs4.element.Tag
        :type maccabi_team_name: str
        :type not_maccabi_team_name: str
        :type maccabi_score: int
        :type not_maccabi_score: int
        :return: MaccabiTeam, NotMaccabiTeam
        :rtype: MaccabiSiteTeamInGame, MaccabiSiteTeamInGame
        """

        maccabi_team_in_game = MaccabiSiteTeamParser.parse_team(bs_content.select("article div.teams div.p50.yellow"),
                                                                maccabi_team_name, maccabi_score)

        not_maccabi_team_in_game = MaccabiSiteTeamParser.parse_team(
            [div for div in bs_content.select("article div.teams div.p50") if "yellow" not in div["class"]],
            not_maccabi_team_name, not_maccabi_score)

        return maccabi_team_in_game, not_maccabi_team_in_game

    @staticmethod
    def __get_referee(bs_content):
        """"
        :type bs_content: bs4.element.Tag
        :rtype: str.
        """

        referee_div_bs = bs_content.select_one("div.info div.referee")
        if referee_div_bs:
            return referee_div_bs.get_text().strip()
        else:
            return "Cant found referee"

    @staticmethod
    def __get_crowd(bs_content):
        """"
        :type bs_content: bs4.element.Tag
        :rtype: str.
        """

        crowd_div_bs = bs_content.select_one("div.info div.viewers")
        if crowd_div_bs:
            return crowd_div_bs.get_text().strip()
        else:
            return "Cant found crowd"
