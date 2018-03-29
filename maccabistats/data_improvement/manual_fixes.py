import logging

logger = logging.getLogger(__name__)

_referees_name_fixes = [("איתן שמואלביץ", ["איתן שמואלביץ'", "שמואלביץ איתן"]),
                        ("רועי ריינשרייבר", ["רועי רנשרייבר"]),
                        ("גל לייבוביץ", ["גל לייבוביץ'", "גל ליבוביץ'"]),
                        ("חיים ליפקוביץ", ["חיים ליפקוביץ'"]),
                        ("ג'ורג' אשקר", ["גורג' אשקר"]),
                        ("איבן בבק", ["איבאן בבק"]),
                        ("סרג' גומייני", ["סרג גומיני", "סרג' גאמייני"]),
                        ("רחמים דינאצ'י", ["רחמים דיאנצ'י"]),
                        ]


def __fix_opponents_names(game):
    if game.not_maccabi_team.name == "עירוני קרית שמונה":
        game.not_maccabi_team.name = "עירוני קריית שמונה"
        logger.info("Fix עירוני קרית שמונה->עירוני קריית שמונה")


def __fix_referees_names(game):
    for referee_best_name, referee_similar_names in _referees_name_fixes:
        if game.referee in referee_similar_names:
            logger.info("Changing referee name from :{old}-->{new}".format(old=game.referee, new=referee_best_name))
            game.referee = referee_best_name


def run_manual_fixes(maccabi_games_stats):
    """
    After running manually all the improvements im data_improvements those fixes added one by one manually.
    :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    for game in maccabi_games_stats.games:
        __fix_opponents_names(game)
        __fix_referees_names(game)

    return maccabi_games_stats
