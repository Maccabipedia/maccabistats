# -*- coding: utf-8 -*-


from maccabistats import *

if __name__ == "__main__":
    run_maccabipedia_source()
    m = load_from_maccabipedia_source()

    """
    m = load_from_maccabipedia_source()
    g = get_maccabi_stats_as_newest_wrapper()

    g.players_streaks.get_players_with_best_goal_assisting_streak()
    m.players_streaks.get_players_with_best_goal_assisting_streak()

    a = 6"""


