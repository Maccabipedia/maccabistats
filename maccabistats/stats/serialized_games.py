# -*- coding: utf-8 -*-

from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from maccabistats.parse.parse_from_all_sites import parse_maccabi_games_from_all_sources

import pickle
import os
import glob
import datetime
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

_maccabistats_root_folder_path = Path.home().as_posix()
_serialized_maccabi_games_folder_path = os.path.join(_maccabistats_root_folder_path, "maccabistats")
_serialized_maccabi_games_file_name_pattern = "maccabi-{version}-{date}.games"
_serialized_maccabi_games_file_path_pattern = os.path.join(_serialized_maccabi_games_folder_path,
                                                           _serialized_maccabi_games_file_name_pattern)


def get_maccabi_stats_as_newest_wrapper(file_name=None):
    """"
    Returns the serialized file_name cast to the latest MaccabiGamesStats object, which means that newer functions can be used.
    """

    return MaccabiGamesStats(get_maccabi_stats(file_name).games)


def get_maccabi_stats(file_name=None):
    """
    :param file_name: pickled maccabi games (probably MaccabiGamesStats object).
                      When no file is given, Try to load the latest maccabi*.games from the default folder.
    :rtype: MaccabiGamesStats
    """

    if not file_name:
        maccabi_games_files_in_default_folder = glob.glob(_serialized_maccabi_games_file_path_pattern.format(version="*", date="*"))
        if not maccabi_games_files_in_default_folder:
            raise RuntimeError(
                f"No file name was given -> Failed to get the latest maccabi*.games from default folder: {_serialized_maccabi_games_folder_path}")
        file_name = maccabi_games_files_in_default_folder[-1]

    else:
        if not os.path.isfile(file_name):
            raise RuntimeError("You should have maccabi.games serialized object, you can use maccabistats.serialize_maccabi_games() to do that.")

    with open(file_name, 'rb') as f:
        logger.info(f"Loading maccabi games from {file_name}")
        return pickle.load(f)


def combine_maccabi_stats_sources():
    """
    Combine all the serialized object from all sources to one maccabi games stats objects, this function should be fast - without rerunning sources.
    :return: MaccabiGamesStats
    """

    return parse_maccabi_games_from_all_sources(without_rerunning=True)


def run_all_maccabi_stats_sources():
    """
    Runs all the sources  - does not use the serialized objects is there are any.
    :return: MaccabiGamesStats
    """

    return parse_maccabi_games_from_all_sources()


def serialize_maccabi_games(maccabi_games_stats, folder_path=_serialized_maccabi_games_folder_path):
    """
    Reserialize maccabi games stats, after doing manually manipulation (run_manual_fixes) or anything else.
    :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    :param folder_path: Folder path to pickle maccabi game at
    """

    if not isinstance(maccabi_games_stats, MaccabiGamesStats):
        raise RuntimeError("You Should serialize only maccabi games stats object")

    file_name = os.path.join(folder_path, _serialized_maccabi_games_file_name_pattern).format(version=maccabi_games_stats.version,
                                                                                              date=str(datetime.date.today()))
    with open(file_name, 'wb') as f:
        pickle.dump(maccabi_games_stats, f)

    logger.info(f"Serialized maccabi games to {file_name}")
