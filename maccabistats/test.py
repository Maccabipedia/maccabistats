# -*- coding: utf-8 -*-


from maccabistats import *

if __name__ == "__main__":
    g = get_maccabi_stats_as_newest_wrapper()
    b = g.player_streaks.get_players_with_best_unbeaten_streak()

    c=6



