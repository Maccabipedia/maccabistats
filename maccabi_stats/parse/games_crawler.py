#!/usr/bin/python
# -*- coding: utf-8 -*-

from maccabi_stats.stats.maccabi_games_stats import MaccabiGamesStats

import pickle
import os


def get_all_the_stuff():
    pickled_data_folder_path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(pickled_data_folder_path, "all-data.pickle"), 'rb') as f:
        return pickle.load(f)


def get_all_stuff_wrapped():
    return MaccabiGamesStats(get_all_the_stuff())
