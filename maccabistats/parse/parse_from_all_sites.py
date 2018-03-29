# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.main_parser import get_parsed_maccabi_games_from_maccabi_site
from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from maccabistats.data_improvement.manual_fixes import run_manual_fixes

import logging

logger = logging.getLogger(__name__)


def parse_maccabi_games_from_all_sites():
    """ Iterate all the sites and merge the output to one list of maccabi games.
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    logger.info("Starting to parse data from all sites.")

    logger.info("Starting to parse data from maccabi-tlv site.")
    maccabi_games_from_maccabi_tlv_site = get_parsed_maccabi_games_from_maccabi_site()
    maccabi_stats_games = MaccabiGamesStats(maccabi_games_from_maccabi_tlv_site)

    maccabi_stats_games_after_manual_fixes = run_manual_fixes(maccabi_stats_games)

    return maccabi_stats_games_after_manual_fixes
