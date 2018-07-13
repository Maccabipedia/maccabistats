from .maccabilogging import initialize_logging

# This should stays first to enable logging across all package
initialize_logging()

from .stats.serialized_games import get_maccabi_stats, get_maccabi_stats_as_newest_wrapper, serialize_maccabi_games
from .parse.parse_from_all_sites import merge_maccabi_games_from_all_serialized_sources, rerun_sources
from .maccabilogging import faster_logging
from maccabistats.data_improvement.manual_fixes import run_general_fixes
