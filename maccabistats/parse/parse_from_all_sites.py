#!/usr/bin/python
# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.main_parser import get_parsed_maccabi_games_from_maccabi_site
from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats

import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def parse_maccabi_games_from_all_sites():
    """ Iterate all the sites and merge the output to one list of maccabi games.
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    logging.info("Starting to parse data from all sites.")

    logging.info("Starting to parse data from maccabi-tlv site.")
    maccabi_games_from_maccabi_tlv_site = get_parsed_maccabi_games_from_maccabi_site()
    return MaccabiGamesStats(maccabi_games_from_maccabi_tlv_site)
