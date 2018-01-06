#!/usr/bin/python
# -*- coding: utf-8 -*-

from maccabi_stats.parse.maccabi_tlv_site.game_parser import MaccabiSiteGameParser

import os
import requests
from bs4 import BeautifulSoup

maccabi_season_games_page_pattern = \
    u"https://www.maccabi-tlv.co.il/משחקים-ותוצאות/הקבוצה-הבוגרת/תוצאות/?season={season_number}#content"

folder_to_save_seasons_html_files = r"F:\maccabi-code\seasons"
folder_to_save_seasons_html_files_pattern = os.path.join(folder_to_save_seasons_html_files, "season-{season_number}")


def get_seasons_games_html_wrapped(season_link):
    """
    :param season_link: str
    :rtype: list of bs4.element.Tag
    """
    if os.path.isfile(season_link):
        with open(season_link, encoding="utf-8") as f:
            data = f.read()
        soup = BeautifulSoup(data, "html.parser")
    else:
        html_content = requests.get(season_link).content
        soup = BeautifulSoup(html_content, "html.parser")

    return soup.find_all("article")


def enumerate_maccabi_site_seasons_web_pages():
    """
    :rtype: tuple of (str, int)
    """
    max_season_number = 80
    for season_number in range(max_season_number):
        yield maccabi_season_games_page_pattern.format(season_number=season_number), season_number


def enumerate_maccabi_site_seasons_files():
    """
    :rtype: tuple of (str, int)
    """
    max_season_number = 80
    for season_number in range(max_season_number):
        yield folder_to_save_seasons_html_files_pattern.format(season_number=season_number), season_number


def get_parsed_maccabi_site_seasons():
    maccabi_games = []
    print("starting!")
    for maccabi_season_web_page, _ in enumerate_maccabi_site_seasons_files():
        print("Parsing season : \n {site}".format(site=maccabi_season_web_page))
        wrapped_season_games = get_seasons_games_html_wrapped(maccabi_season_web_page)
        print("Found {number} games on this season!\n".format(number=len(wrapped_season_games)))

        for game in wrapped_season_games:
            m = MaccabiSiteGameParser.parse_game(game)
            maccabi_games.append(m)

    return maccabi_games


def save_all_maccabi_seasons_web_pages_to_disk():
    for maccabi_season_web_page, season_number in enumerate_maccabi_site_seasons_web_pages():
        with open(folder_to_save_seasons_html_files_pattern.format(season_number=season_number),
                  'wb') as maccabi_site_file:
            print("Writing {file_name} to disk".format(file_name=maccabi_season_web_page))
            html_content = requests.get(maccabi_season_web_page).content
            maccabi_site_file.write(html_content)
