# -*- coding: utf-8 -*-


from maccabistats.stats.serialized_games import get_maccabi_stats

if __name__ == "__main__":

    g = get_maccabi_stats()
    g.try_wins()
    b = 6
