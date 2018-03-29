# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.game_squads_parser import MaccabiSiteGameSquadsParser
from maccabistats.parse.maccabi_tlv_site.config import get_max_seasons_from_settings, \
    get_season_page_pattern_from_settings, get_folder_to_save_seasons_html_files_from_settings, \
    get_should_use_disk_to_crawl_when_available_from_settings

import os
import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

folder_to_save_seasons_html_files_pattern = os.path.join(get_folder_to_save_seasons_html_files_from_settings(),
                                                         "season-{season_number}")


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
    for season_number in range(get_max_seasons_from_settings()):
        season_web_page_link = get_season_page_pattern_from_settings().format(season_number=season_number)
        yield requests.get(season_web_page_link).content


def __get_parsed_maccabi_games_from_web():
    """ Parse maccabi games from maccabi site.
    :rtype: list of maccabistats.models.game_data.GameData
    """

    maccabi_games = []
    for season_number, season_web_page_content in enumerate(__enumerate_season_web_pages_content_from_web()):
        logger.info("Parsing season number {s_n}".format(s_n=season_number))
        maccabi_games.extend(__parse_games_from_season_page_content(season_web_page_content))

    return maccabi_games


def __parse_games_from_season_page_content(maccabi_season_web_page_content):
    bs_games_elements = __extract_games_bs_elements(maccabi_season_web_page_content)
    logger.info("Found {number} games on this season!".format(number=len(bs_games_elements)))

    return [MaccabiSiteGameSquadsParser.parse_game(bs_game_element) for bs_game_element in bs_games_elements]


def get_parsed_maccabi_games_from_maccabi_site():
    try:
        logger.info("Trying to iterate seasons pages from web")
        return __get_parsed_maccabi_games_from_web()
    except Exception:
        logger.exception("Exception while trying to parse maccabi-tlv site pages from web.")

    raise Exception("Could not parse maccabi games from disk or web")


# Might be deprecated
def save_maccabi_seasons_web_pages_to_disk(folder_path=folder_to_save_seasons_html_files_pattern):
    """
    Iterate over maccabi site seasons link and saves them to disk
    :param folder_path: where to save the html files.
    """
    for season_number in range(get_max_seasons_from_settings()):
        season_web_page_link = get_season_page_pattern_from_settings().format(season_number=season_number)
        season_web_page_content = requests.get(season_web_page_link).content

        logger.info("Writing {file_name} to disk".format(file_name=season_web_page_link))
        with open(folder_path.format(season_number=season_number), 'wb') as maccabi_site_file:
            maccabi_site_file.write(season_web_page_content)
