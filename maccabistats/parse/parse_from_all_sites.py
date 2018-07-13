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


def rerun_sources(sources_to_run=None):
    """
    Rerun maccabi games sources, each source will serialize the data after rerunning.

    :param sources_to_run: Names of the sources to run, should be taken from - maccabistats.parse.sources.SourcesNames.
                           All the sources will be rerun as default.
    :type sources_to_run: list or string
    """

    logger.info("Validating setup for crawling is ready.")
    __validate_folders_to_save_maccabi_games_exists()

    maccabistats_sources = [MaccabiTlvSiteSource(), TableSource()]
    if sources_to_run:
        if type(sources_to_run) is not list:
            sources_to_run = [sources_to_run]
        maccabistats_sources = filter(lambda s: s.name in sources_to_run, maccabistats_sources)

    for source in maccabistats_sources:
        logger.info("Parsing the source: {name}".format(name=source.name))
        source.parse_maccabi_games()
        source.run_general_fixes()
        source.run_specific_fixes()

        logger.info("Loading the source: {name}".format(name=source.name))
        source.serialize_games()

    logger.info("Parsed all the sources")


def merge_maccabi_games_from_all_serialized_sources():
    """
    Assumes all the sources serialized their data (by calling "run_all_sources" or have somehow the serialized data).
    Iterate all the sources and merge the maccabi games stats (after running general&specific fixes) to one list of maccabi games.

    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    logger.info("Validating setup for crawling is ready.")

    maccabi_games_stats_from_all_sources = []
    maccabistats_sources = [MaccabiTlvSiteSource(), TableSource()]
    for source in maccabistats_sources:
        logger.info("Loading the source: {name}".format(name=source.name))
        source.load_serialized_games()
        source.run_general_fixes()
        source.run_specific_fixes()

        maccabi_games_stats_from_all_sources.append(source.maccabi_games_stats)

    # todo: write merge logic

    logger.info("Merging all the sources to one maccabi games stats")
    merged_maccabistats_games = merge_maccabitlv_and_table(maccabi_games_stats_from_all_sources[0], maccabi_games_stats_from_all_sources[1])
    logger.info("Running general fixes on merged maccabi games stats object")

    maccabistats_games = run_general_fixes(MaccabiGamesStats(merged_maccabistats_games))
    return maccabistats_games
