from .maccabilogging import initialize_logging

# This should stays first to enable logging across all package
initialize_logging()

from .stats.serialized_games import serialize_maccabi_games, get_maccabi_stats, get_maccabi_stats_as_newest_wrapper
from .maccabilogging import faster_logging
from maccabistats.data_improvement.manual_fixes import run_manual_fixes
