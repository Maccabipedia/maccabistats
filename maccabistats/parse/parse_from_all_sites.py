# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.main_parser import get_parsed_maccabi_games_from_maccabi_site
from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats

import logging
import os
from pathlib import Path

log_root_folder_path = Path.home().as_posix()
log_file_path = os.path.join(log_root_folder_path, "maccabistats-logs", "maccabistats.log")
log_file_folder_path = os.path.dirname(log_file_path)

if not os.path.isdir(log_file_folder_path):
    os.makedirs(log_file_folder_path)

logger = logging.getLogger()
main_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


warning_handler = logging.FileHandler(log_file_path, 'w', encoding="utf-8")
warning_handler.setFormatter(main_formatter)
warning_handler.setLevel(logging.INFO)

logger.addHandler(warning_handler)


def parse_maccabi_games_from_all_sites():
    """ Iterate all the sites and merge the output to one list of maccabi games.
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    logger.info("Starting to parse data from all sites.")

    logger.info("Starting to parse data from maccabi-tlv site.")
    maccabi_games_from_maccabi_tlv_site = get_parsed_maccabi_games_from_maccabi_site()
    return MaccabiGamesStats(maccabi_games_from_maccabi_tlv_site)
