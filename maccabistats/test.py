# -*- coding: utf-8 -*-


from maccabistats.stats.serialized_games import get_maccabi_stats, serialize_maccabi_games
from maccabistats.maccabilogging import faster_logging

if __name__ == "__main__":
    # faster_logging()
    g = get_maccabi_stats()

    f = g.get_first_league_games()
    total = f.streaks.get_similar_losses_streak_by_length(3)
    b = total[1]
    a = 6
