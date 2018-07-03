import logging
from maccabistats.parse.maccabistats_source import MaccabiStatsSource
from maccabistats.parse.table.main_parser import get_parsed_maccabi_games_from_json

logger = logging.getLogger(__name__)

"""
Table is external source which saves maccabi games as json
"""


class TableSource(MaccabiStatsSource):

    def parse_maccabi_games(self, without_rerunning=False):
        """
        Parse the raw data and saves it on self.maccabi_games_stats.

        :param without_rerunning: whether this source should be rerun or just use the serialized object.
        """

        super().parse_maccabi_games(without_rerunning=False)

    def _rerun_source(self):
        """
        Parse the raw data and saves it on self.maccabi_games_stats
        """

        return get_parsed_maccabi_games_from_json()

    def run_specific_fixes(self):
        """
        Run any specific fixes for this source (such as error within the raw data).
        """

        logger.info("ATM, there are not specific fixes for table source")

