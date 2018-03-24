from .maccabilogging import initialize_logging

# This should stays first to enable logging across all package
initialize_logging()

from .stats.serialized_games import serialize_maccabi_games, get_maccabi_stats
from .maccabilogging import faster_logging
