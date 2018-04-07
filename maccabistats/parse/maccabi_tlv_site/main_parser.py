# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.game_squads_parser import MaccabiSiteGameSquadsParser
from maccabistats.parse.maccabi_tlv_site.config import get_max_seasons_from_settings, \
    get_season_page_pattern_from_settings, get_folder_to_save_seasons_html_files_from_settings, \
    get_use_lxml_parser_from_settings, get_use_multi_process_crawl_from_settings, get_crawling_processes_number_from_settings
from maccabistats.maccabilogging import initialize_logging_for_this_process

import os
import requests
import logging
from bs4 import BeautifulSoup
from multiprocessing import Pool
import itertools

logger = logging.getLogger(__name__)

folder_to_save_seasons_html_files_pattern = os.path.join(get_folder_to_save_seasons_html_files_from_settings(),
                                                         "season-{season_number}")


def __get_beautifulsoup_parser_name():
    if get_use_lxml_parser_from_settings():
        logger.info("Using lxml parser for beautifulsoup")
        return "lxml"
    else:
        logger.info("Using html.parser for beautifulsoup")
        return "html.parser"


def __extract_games_bs_elements(season_web_page_content):
    """
    :param season_web_page_content: str
    :rtype: list of bs4.element.Tag
    """

    soup = BeautifulSoup(season_web_page_content, __get_beautifulsoup_parser_name())
    return soup.find_all("article")


def __get_season_web_page_content_by_season_number(season_number):
    """
    Returns the current season number page content
    :param season_number: season number to be requested.
    :type season_number: int
    :return: bytes
    """

    season_web_page_link = get_season_page_pattern_from_settings().format(season_number=season_number)
    return requests.get(season_web_page_link).content


def __get_parsed_maccabi_games_from_web():
    """ Parse maccabi games from maccabi site.
    :rtype: list of maccabistats.models.game_data.GameData
    """

    maccabi_games = []
    for season_number in range(get_max_seasons_from_settings()):
        logger.info("Parsing season number {s_n}".format(s_n=season_number))
        maccabi_games.extend(__parse_games_from_season_number(season_number))

    return maccabi_games


def __get_season_string_from_season_page_content(season_web_page_content):
    soup = BeautifulSoup(season_web_page_content, __get_beautifulsoup_parser_name())
    # TODO try except that better
    wrapped_season_string = soup.select("main div.dropdown a")[0].get_text()
    season_string = wrapped_season_string.strip("כל העונות()")

    return season_string


def __get_parsed_maccabi_games_from_web_multi_process():
    """
    Parse maccabi games same as __get_parsed_maccabi_games_from_web, just with multiprocess.
    :return: list of maccabistats.models.game_data.GameData
    """

    crawling_processes = get_crawling_processes_number_from_settings()
    logger.info("Crawling with {num} processes".format(num=crawling_processes))

    maccabi_seasons_numbers = range(get_max_seasons_from_settings())
    logger.info("Starting to parse games using multi processes.")
    with Pool(crawling_processes) as pool:
        maccabi_games = list(itertools.chain.from_iterable(pool.map(__parse_games_from_season_number, maccabi_seasons_numbers)))
    logger.info("Finished to parse games using multi processes.")

    from maccabistats.maccabilogging import merge_logs_files_from_all_processes
    merge_logs_files_from_all_processes()

    return maccabi_games


def __parse_games_from_season_number_multi_process(*args, **kwargs):

    __parse_games_from_season_number(*args, **kwargs)


def __parse_games_from_season_number(season_number):
    initialize_logging_for_this_process()
    logger.info("Refreshed logging handlers in this process!")

    maccabi_season_web_page_content = __get_season_web_page_content_by_season_number(season_number)

    bs_games_elements = __extract_games_bs_elements(maccabi_season_web_page_content)
    season_string = __get_season_string_from_season_page_content(maccabi_season_web_page_content)
    logger.info("Found {number} games on this season! {season}".format(number=len(bs_games_elements), season=season_string))

    return [MaccabiSiteGameSquadsParser.parse_game(bs_game_element, season_string) for bs_game_element in bs_games_elements]


def get_parsed_maccabi_games_from_maccabi_site():
    try:
        logger.info("Trying to iterate seasons pages from web")
        if get_use_multi_process_crawl_from_settings():
            logger.info("Crawling maccabi games with multi process!")
            return __get_parsed_maccabi_games_from_web_multi_process()
        else:
            logger.info("Crawling maccabi games with one process!")
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
