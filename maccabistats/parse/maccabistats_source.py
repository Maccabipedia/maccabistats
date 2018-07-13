from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from maccabistats.data_improvement.manual_fixes import run_general_fixes
import logging
import os
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)

home_folder = Path.home().as_posix()
serialized_sources_path_pattern = os.path.join(home_folder, "maccabistats", "sources", "{source_name}.games")

"""
This class is responsible to set the api for each maccabistats source, the common usage should be :

m = MaccabiStatsSource()
m.parse_maccabi_games()
m.run_general_fixes()
m.run_specific_fixes()

games = m.maccabi_games_stats
"""


class MaccabiStatsSource(object):
    def __init__(self, name):
        self.name = name
        self.maccabi_games_stats = None
        self._serialized_games_path = serialized_sources_path_pattern.format(source_name=self.name)

    def parse_maccabi_games(self):
        """
        Parse the raw data and saves it on self.maccabi_games_stats.
        """

        logger.info(f"Starting to parse maccabi games from :{self.name}")
        parsed_games = self._rerun_source()
        self.maccabi_games_stats = MaccabiGamesStats(parsed_games)
        self.serialize_games()

    def _rerun_source(self):
        """
        Parse the raw data and saves it on self.maccabi_games_stats
        :return:
        """

        raise NotImplementedError()

    def run_specific_fixes(self):
        """
        Run any specific fixes for this source (such as error within the raw data).
        """

        raise NotImplementedError()

    def run_general_fixes(self):
        """
        Runs any general fixes that relevant for all sources (such as naming and so on).
        """

        if self.maccabi_games_stats is None:
            raise RuntimeError("You should run parse_maccabi_games first.")

        self.maccabi_games_stats = run_general_fixes(self.maccabi_games_stats)

    def load_serialized_games(self):
        """
        Load the serialized games to self.maccabi_games_stats
        :return: MaccabiGamesStats
        """

        with open(self._serialized_games_path, 'rb') as f:
            self.maccabi_games_stats = pickle.load(f)

    def serialize_games(self):
        """
        Serialize the parsed games (without any fixes).
        """

        if os.path.isfile(self._serialized_games_path):
            # todo: bkup the old file
            # old_file_path = Path(self._serialized_games_path)
            # old_file_path.stem+= int(time())
            pass

        with open(self._serialized_games_path, 'wb') as f:
            pickle.dump(self.maccabi_games_stats, f)
