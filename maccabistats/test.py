# -*- coding: utf-8 -*-


def stuff():
    from maccabistats import get_maccabi_stats_as_newest_wrapper
    g = get_maccabi_stats_as_newest_wrapper()
    b = g.players_streaks.get_players_with_best_unbeaten_streak()
    print(b)


def prof():
    import cProfile

    pr = cProfile.Profile()
    pr.enable()

    # Your function
    stuff()

    pr.disable()
    # after your program ends
    pr.print_stats(sort="calls")


if __name__ == "__main__":
    stuff()

