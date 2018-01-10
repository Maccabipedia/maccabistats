# -*- coding: utf-8 -*-

from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from maccabistats.parse.parse_from_all_sites import parse_maccabi_games_from_all_sites

import pickle
import os

serialized_maccabi_games_folder_path = os.path.dirname(os.path.abspath(__file__))
serialized_maccabi_games_file_name = "maccabi.games"
serialized_maccabi_games_file_path = os.path.join(serialized_maccabi_games_folder_path,
                                                  serialized_maccabi_games_file_name)


def get_maccabi_stats(file_name=serialized_maccabi_games_file_path):
    """
    :param file_name: pickled maccabi games (probably MaccabiGamesStats object).
    :rtype: MaccabiGamesStats
    """
    with open(file_name, 'rb') as f:
        return MaccabiGamesStats(pickle.load(f))


def serialize_maccabi_games(file_name=serialized_maccabi_games_file_path):
    """
    :param file_name: pickled maccabi games path.
    """

    maccabi_games = parse_maccabi_games_from_all_sites()
    with open(file_name, 'wb') as f:
        pickle.dump(maccabi_games, f)
