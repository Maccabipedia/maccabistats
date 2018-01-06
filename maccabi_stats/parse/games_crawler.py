#!/usr/bin/python
# -*- coding: utf-8 -*-

from maccabi_stats.stats.maccabi_site_games_wrapper import MaccabiSiteGamesWrapper

import pickle
import os


def get_all_the_stuff():
    pickled_data_folder_path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(pickled_data_folder_path, "all-data.pickle"), 'rb') as f:
        return pickle.load(f)


def get_all_stuff_wrapped():
    return MaccabiSiteGamesWrapper(get_all_the_stuff())
