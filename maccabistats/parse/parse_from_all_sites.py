# -*- coding: utf-8 -*-

from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from maccabistats.parse.maccabi_tlv_site.maccabi_tlv_site_source import MaccabiTlvSiteSource
from maccabistats.parse.table.table_source import TableSource
from maccabistats.parse.maccabi_tlv_site.config import get_folder_to_save_games_html_files_from_settings, \
    get_folder_to_save_seasons_html_files_from_settings
from maccabistats.parse.merge_sources import merge_maccabitlv_and_table
from maccabistats.data_improvement.manual_fixes import run_general_fixes

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


def parse_maccabi_games_from_all_sources(without_rerunning=False):
    """
    Iterate all the sources and merge the output to one list of maccabi games.

    :param without_rerunning: whether the sources should be just "combined" from the serialized object on the disk
                              or rerun again (might be long operation).
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    logger.info("Validating setup for crawling is ready.")
    __validate_folders_to_save_maccabi_games_exists()

    maccabi_games_stats_from_all_sources = []
    maccabistats_sources = [MaccabiTlvSiteSource("Maccabi-tlv site"), TableSource("Table-jsoned")]
    for source in maccabistats_sources:
        logger.info("Handle the source: {name}".format(name=source.name))
        source.parse_maccabi_games(without_rerunning=without_rerunning)
        source.run_general_fixes()
        source.run_specific_fixes()

        maccabi_games_stats_from_all_sources.append(source.maccabi_games_stats)

    # todo: write merge logic

    logger.info("Merging all the sources to one maccabi games stats")
    merged_maccabistats_games = merge_maccabitlv_and_table(maccabi_games_stats_from_all_sources[0], maccabi_games_stats_from_all_sources[1])
    logger.info("Running general fixes on merged maccabi games stats object")

    maccabistats_games = run_general_fixes(MaccabiGamesStats(merged_maccabistats_games))
    return maccabistats_games
