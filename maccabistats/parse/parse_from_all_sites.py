# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.main_parser import get_parsed_maccabi_games_from_maccabi_site
from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats

import logging
import os

log_file_path = os.path.join(os.environ["appdata"], "maccabistats", "maccabistats.log")
logger = logging.getLogger()
main_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


warning_handler = logging.FileHandler(log_file_path, 'w', encoding="utf-8")
warning_handler.setFormatter(main_formatter)
warning_handler.setLevel(logging.WARNING)

logger.addHandler(warning_handler)


def parse_maccabi_games_from_all_sites():
    """ Iterate all the sites and merge the output to one list of maccabi games.
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    logger.info("Starting to parse data from all sites.")

    logger.info("Starting to parse data from maccabi-tlv site.")
    maccabi_games_from_maccabi_tlv_site = get_parsed_maccabi_games_from_maccabi_site()
    return MaccabiGamesStats(maccabi_games_from_maccabi_tlv_site)
