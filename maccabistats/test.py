# -*- coding: utf-8 -*-


from maccabistats.stats.serialized_games import get_maccabi_stats

if __name__ == "__main__":

    g = get_maccabi_stats()
    g[100].events
    g.home_games.players.most_winner_by_percentage[0:5]
    a=6
