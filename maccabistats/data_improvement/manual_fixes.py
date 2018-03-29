

def run_manual_fixes(maccabi_games_stats):
    """
    After running manually all the improvements im data_improvements those fixes added one by one manually.
    :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    for game in maccabi_games_stats.games:
        if game.not_maccabi_team.name == "עירוני קרית שמונה":
            game.not_maccabi_team.name = "עירוני קריית שמונה"
            print("Fix עירוני קרית שמונה->עירוני קריית שמונה")

    return maccabi_games_stats

