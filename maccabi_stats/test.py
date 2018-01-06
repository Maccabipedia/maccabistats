from maccabi_stats.games_crawler import get_all_stuff_wrapped


if __name__ == "__main__":
    games = get_all_stuff_wrapped()
    old = games.played_before("1.1.2000")
    print(old.best_scorers)
