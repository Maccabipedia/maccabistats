# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.main_parser import get_parsed_maccabi_games_from_maccabi_site
from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from maccabistats.data_improvement.manual_fixes import run_manual_fixes
from maccabistats.parse.maccabi_tlv_site.config import get_folder_to_save_games_html_files_from_settings, \
    get_folder_to_save_seasons_html_files_from_settings

import logging
import os

logger = logging.getLogger(__name__)


def __validate_folders_to_save_maccabi_games_exists():
    """
    Makes sure that the folders (from settings) that given to save the game & season exists
    """

    folder_to_save_seasons = get_folder_to_save_seasons_html_files_from_settings()
    folder_to_save_games = get_folder_to_save_games_html_files_from_settings()

    if not os.path.exists(folder_to_save_seasons):
        logger.info("The folder from settings to save the seasons in does not exists, creating : {path}".format(path=folder_to_save_seasons))
        os.makedirs(folder_to_save_seasons)

    if not os.path.exists(get_folder_to_save_games_html_files_from_settings()):
        logger.info("The folder from settings to save the games in does not exists, creating : {path}".format(path=folder_to_save_games))
        os.makedirs(folder_to_save_games)


def parse_maccabi_games_from_all_sites():
    """ Iterate all the sites and merge the output to one list of maccabi games.
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    logger.info("Validating setup for crawling is ready.")
    __validate_folders_to_save_maccabi_games_exists()

    logger.info("Starting to parse data from all sites.")
    logger.info("Starting to parse data from maccabi-tlv site.")

    maccabi_games_from_maccabi_tlv_site = get_parsed_maccabi_games_from_maccabi_site()
    maccabi_stats_games = MaccabiGamesStats(maccabi_games_from_maccabi_tlv_site)

    maccabi_stats_games_after_manual_fixes = run_manual_fixes(maccabi_stats_games)

    return maccabi_stats_games_after_manual_fixes
