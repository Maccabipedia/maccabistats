# -*- coding: utf-8 -*-


from maccabistats.stats.serialized_games import get_maccabi_stats, serialize_maccabi_games
from maccabistats.maccabilogging import faster_logging

if __name__ == "__main__":
    # faster_logging()
    g = get_maccabi_stats()
    s = g.seasons.get_seasons_stats()
    s.sort_by_wins_count()
    print(s)
    a = 6
