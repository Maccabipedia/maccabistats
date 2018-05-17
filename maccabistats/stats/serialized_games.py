# -*- coding: utf-8 -*-

from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from maccabistats.parse.parse_from_all_sites import parse_maccabi_games_from_all_sites

import pickle
import os

serialized_maccabi_games_folder_path = os.path.dirname(os.path.abspath(__file__))
serialized_maccabi_games_file_name = "maccabi.games"
serialized_maccabi_games_file_path = os.path.join(serialized_maccabi_games_folder_path,
                                                  serialized_maccabi_games_file_name)


def get_maccabi_stats_as_newest_wrapper(file_name=serialized_maccabi_games_file_path):
    """"
    Returns the serialized file_name cast to the latest MaccabiGamesStats object, which means that newer functions can be used.
    """

    return MaccabiGamesStats(get_maccabi_stats(file_name).games)


def get_maccabi_stats(file_name=serialized_maccabi_games_file_path):
    """
    :param file_name: pickled maccabi games (probably MaccabiGamesStats object).
    :rtype: MaccabiGamesStats
    """

    if not os.path.isfile(file_name):
        raise RuntimeError("You should have maccabi.games serialized object, you can use maccabistats.serialize_maccabi_games() to do that.")

    with open(file_name, 'rb') as f:
        return pickle.load(f)


def serialize_maccabi_games(file_name=serialized_maccabi_games_file_path):
    """
    :param file_name: pickled maccabi games path.
    """

    maccabi_games = parse_maccabi_games_from_all_sites()
    with open(file_name, 'wb') as f:
        pickle.dump(maccabi_games, f)


def reserialize_maccabi_games(maccabi_games_stats, file_name=serialized_maccabi_games_file_path):
    """
    Reserialize maccabi games stats, after doing manually manipulation (run_manual_fixes) or anything else.
    :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    :param file_name: path to pickle maccabi game at
    """

    if not isinstance(maccabi_games_stats, MaccabiGamesStats):
        raise RuntimeError("You Should serialize only maccabi games stats object")

    with open(file_name, 'wb') as f:
        pickle.dump(maccabi_games_stats, f)
