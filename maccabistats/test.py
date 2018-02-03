# -*- coding: utf-8 -*-


from maccabistats.stats.serialized_games import get_maccabi_stats

if __name__ == "__main__":

    g = get_maccabi_stats()
    pp = g.streaks.get_longest_goals_from_bench_games()
    a=6
