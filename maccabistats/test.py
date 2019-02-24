# -*- coding: utf-8 -*-


from maccabistats import *

if __name__ == "__main__":
    merge_maccabi_games_from_all_input_serialized_sources()
    rerun_sources("MaccabiPedia")

    """
    m = load_from_maccabipedia_source()
    g = get_maccabi_stats_as_newest_wrapper()

    g.players_streaks.get_players_with_best_goal_assisting_streak()
    m.players_streaks.get_players_with_best_goal_assisting_streak()

    a = 6"""


