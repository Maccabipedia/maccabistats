from maccabistats.data_improvement.fix_specific_games import fix_specific_games

import logging

logger = logging.getLogger(__name__)

# The format is like that:  ("real name", ["possible wrongs name", "another one"])
_referees_name_fixes = [("איתן שמואלביץ", ["איתן שמואלביץ'", "שמואלביץ איתן"]),
                        ("רועי ריינשרייבר", ["רועי רנשרייבר"]),
                        ("גל לייבוביץ", ["גל לייבוביץ'", "גל ליבוביץ'"]),
                        ("חיים ליפקוביץ", ["חיים ליפקוביץ'"]),
                        ("ג'ורג' אשקר", ["גורג' אשקר"]),
                        ("איבן בבק", ["איבאן בבק"]),
                        ("סרג' גומייני", ["סרג גומיני", "סרג' גאמייני"]),
                        ("רחמים דינאצ'י", ["רחמים דיאנצ'י"]),
                        ("משה מזרחי", ["משה מיזרחי"]),
                        ("חיים יעקב", ["חיים יעקוב"]),
                        ("יאיר טילינגר", ["יאיר טליגר"]),
                        ("אנדריס טרימאניס", ["אנדריס טריימאניס"]),
                        ("ליאור קורנפלד", ["ליאור קרונפלד"]),
                        ("יהושע לויה", ["יהושוע לויה"]),
                        ("סבי אלנקווה", ["בני אלנקווה"]),
                        ("מרכוס עוזיאל", ["מרקוס עוזיאל"]),
                        ]

# The format is like referees above.
_players_name_fixes = [("מיקו בלו", ["מנחם 'מיקו' בלו"]),
                       ("יוסף מרימוביץ'", ["יוסל'ה מרימוביץ'"]),
                       ("טל בן חיים (הבלם)", ["טל בן חיים"]),
                       ("איציק זוהר", ["זוהר"]),
                       ("בן בן יאיר", ["בן בן-יאיר"]),
                       ("שאול בן דוד", ["שאול בן דויד"]),
                       ("אלירן ג'ורג'", ["אלירן ג'ורג"]),
                       ("גונסאלו גארסיה", ["גונזאלו גארסיה"]),
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


def __fix_competitions_names(game):
    if game.competition == "ליגת לאומית":
        game.competition = "ליגה לאומית"
        logger.info("ליגת לאומית->ליגה לאומית")


def __fix_maccabi_players_names(game):
    for player in game.maccabi_team.players:
        for player_best_name, player_similar_names in _players_name_fixes:
            if player.name in player_similar_names:
                logger.info("Changing player name from :{old}->{new}".format(old=player.name, new=player_best_name))
                player.name = player_best_name


# TODO fix that in crawling
def __fix_seasons(game):
    """
    Remove ' - ' from season and replace it with ' / '.
    """

    if "-" in game.season:
        logger.info("Replacing '-' with '/' in game season")
        game.season = game.season.replace('-', '/')


def run_manual_fixes(maccabi_games_stats):
    """
    After running manually all the improvements im data_improvements those fixes added one by one manually.
    :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    for game in maccabi_games_stats.games:
        __fix_opponents_names(game)
        __fix_referees_names(game)
        __fix_competitions_names(game)
        __fix_maccabi_players_names(game)
        __fix_seasons(game)

    fix_specific_games(maccabi_games_stats)

    return maccabi_games_stats
