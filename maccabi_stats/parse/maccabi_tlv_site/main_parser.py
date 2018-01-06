#!/usr/bin/python
# -*- coding: utf-8 -*-

from maccabi_stats.parse.maccabi_tlv_site.game_parser import MaccabiSiteGameParser

import os
import requests
from bs4 import BeautifulSoup

maccabi_season_page_pattern = \
    u"https://www.maccabi-tlv.co.il/משחקים-ותוצאות/הקבוצה-הבוגרת/תוצאות/?season={season_number}#content"

# TODO - to configuration
folder_to_save_seasons_html_files = r"c:\code\maccabi-backup\seasons"
folder_to_save_seasons_html_files_pattern = os.path.join(folder_to_save_seasons_html_files, "season-{season_number}")

max_seasons_number = 80


def __extract_games_bs_elements(season_web_page_content):
    """
    :param season_web_page_content: str
    :rtype: list of bs4.element.Tag
    """

    soup = BeautifulSoup(season_web_page_content, "html.parser")
    return soup.find_all("article")


def __enumerate_season_web_pages_content_from_web():
    """
    :rtype: tuple of (str, int)
    """
    for season_number in range(max_seasons_number):
        season_web_page_link = maccabi_season_page_pattern.format(season_number=season_number)
        yield requests.get(season_web_page_link).content


def __enumerate_season_web_pages_content_from_disk():
    """
    :rtype: tuple of (str, int)
    # TODO - shouold return tuple with ,season number?
    """
    for season_number in range(max_seasons_number):
        season_web_page_file_path = folder_to_save_seasons_html_files_pattern.format(season_number=season_number)
        with open(season_web_page_file_path, encoding="utf-8") as f:
            yield f.read()


def __get_parsed_maccabi_games_from_web():
    """ Parse maccabi games from maccabi site.
    :rtype: list of maccabi_stats.models.game_data.GameData
    """

    maccabi_games = []
    for season_web_page_content in __enumerate_season_web_pages_content_from_web():
        maccabi_games.extend(__parse_games_from_season_page_content(season_web_page_content))

    return maccabi_games


def __get_parsed_maccabi_games_from_disk():
    """ Parse maccabi games from local html files (path configured at config file).
    :rtype: list of maccabi_stats.models.game_data.GameData
    """
    
    maccabi_games = []
    for season_web_page_content in __enumerate_season_web_pages_content_from_disk():
        maccabi_games.extend(__parse_games_from_season_page_content(season_web_page_content))

    return maccabi_games


def __parse_games_from_season_page_content(maccabi_season_web_page_content):
    bs_games_elements = __extract_games_bs_elements(maccabi_season_web_page_content)
    print("Found {number} games on this season!\n".format(number=len(bs_games_elements)))

    return [MaccabiSiteGameParser.parse_game(bs_game_element) for bs_game_element in bs_games_elements]


def get_parsed_maccabi_games_from_maccabi_site():
    try:
        print("Trying to iterate seasons pages from disk")
        return __get_parsed_maccabi_games_from_disk()
    except Exception as e:
        print("Exception while trying to parse maccabi-tlv site pages from disk {what}".format(what=str(e)))

    try:
        print("Trying to iterate seasons pages from web")
        return __get_parsed_maccabi_games_from_web()
    except Exception as e:
        print("Exception while trying to parse maccabi-tlv site pages from web {what}".format(what=str(e)))

    raise Exception("Could not parse maccabi games from disk or web")


def save_maccabi_seasons_web_pages_to_disk(folder_path=folder_to_save_seasons_html_files_pattern):
    """
    Iterate over maccabi site seasons link and saves them to disk
    :param folder_path: where to save the html files.
    """
    # TODO: add read from config - where to save season links
    for season_number in range(max_seasons_number):
        season_web_page_link = maccabi_season_page_pattern.format(season_number=season_number)
        season_web_page_content = requests.get(season_web_page_link).content

        print("Writing {file_name} to disk".format(file_name=season_web_page_link))
        with open(folder_path.format(season_number=season_number), 'wb') as maccabi_site_file:
            maccabi_site_file.write(season_web_page_content)
