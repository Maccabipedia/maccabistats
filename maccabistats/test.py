# -*- coding: utf-8 -*-


from maccabistats import *

if __name__ == "__main__":

    g = get_maccabi_stats_as_newest_wrapper()

    b = g.graphs.goals_distribution_for_player("ערן זהבי")
    print(b[0:10])

    a = 6
