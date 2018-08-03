from maccabistats.models.player_game_events import GameEventTypes, GoalGameEvent
from maccabistats.parse.teams_names_changer import teams_names_changer

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

# The format is like players above.
_competitions_name_fixes = [("גביע אירופה למחזיקות גביע", ["גביע אירופה למחזיקות"]),
                            ("מוקדמות הליגה האירופית", ["מוקדמות ליגה אירופית"]),
                            ("גביע אסיה לאלופות", ["גביע אסיה"]),
                            ("פלייאוף הליגה האירופית", ["פלייאוף אירופה ליג"]),
                            ("גביע אופא", ['גביע אופ"א']),
                            ("הליגה האירופית", ["ליגה אירופית"]),
                            ("ליגת העל", ["ליגת Winner"]),
                            ("ליגה לאומית", ["ליגת לאומית"]),
                            ("ליגה א", ["ליגה א'"]),
                            ]


def __fix_teams_names(game):
    if game.not_maccabi_team.name in teams_names_changer:
        old_team_name = game.not_maccabi_team.name
        game.not_maccabi_team.name = teams_names_changer[old_team_name].change_name(game)
        # Some teams names wont be changed (because the mapping is between team original name and the team name along the years)
        if old_team_name != game.not_maccabi_team.name:
            logger.info(f"Changing {'Home' if game.is_maccabi_home_team else 'Away'} team name from :{old_team_name}-->{game.not_maccabi_team.name}")


def __fix_referees_names(game):
    for referee_best_name, referee_similar_names in _referees_name_fixes:
        if game.referee in referee_similar_names:
            logger.info("Changing referee name from :{old}-->{new}".format(old=game.referee, new=referee_best_name))
            game.referee = referee_best_name


def __fix_competitions_names(game):
    for competition_best_name, competition_similar_name in _competitions_name_fixes:
        if game.competition in competition_similar_name:
            logger.info("Changing competition name from :{old}-->{new}".format(old=game.competition, new=competition_best_name))
            game.competition = competition_best_name


def __fix_maccabi_players_names(game):
    for player in game.maccabi_team.players:
        for player_best_name, player_similar_names in _players_name_fixes:
            if player.name in player_similar_names:
                logger.info("Changing player name from :{old}->{new}".format(old=player.name, new=player_best_name))
                player.name = player_best_name


def __fix_fixtures(game):
    # If game played in the first league
    if game.competition in ["ליגת העל", "ליגה לאומית", "ליגת Winner", "ליגה א'"]:
        if isinstance(game.fixture, int):
            logger.info(f"Adding 'מחזור' prefix to the ame at {game.date})")
            game.fixture = f"מחזור {game.fixture}"


def __fix_seasons(game):
    """
    Remove ' - ' from season and replace it with ' / '.
    """

    if "-" in game.season:
        logger.info("Replacing '-' with '/' in game season")
        game.season = game.season.replace('-', '/')


def __fix_half_parsed_goal_events(game):
    half_parsed_goals = [event for event in game._half_parsed_events if event['event_type'] == GameEventTypes.GOAL_SCORE]
    if not half_parsed_goals:
        return

    total_score = game.maccabi_team.score + game.not_maccabi_team.score
    total_goal_events = len(game.goals())

    if total_score != total_goal_events:
        logger.info("Found game (date-{date}) with "
                    "total score of: {total_score}, total goals events: {total_goal_events} and total half parsed goals: {total_half_parsed_goals}"
                    .format(date=game.date, total_score=total_score, total_goal_events=total_goal_events,
                            total_half_parsed_goals=len(half_parsed_goals)))
    else:
        logger.warning("Total score & total goals events are equals "
                       "but game (date-{date}) got {num} half parsed goals.".format(date=game.date, num=len(half_parsed_goals)))

    if total_goal_events + len(half_parsed_goals) <= total_score:
        logger.info("Half parsed goal events seems to missing goals, Adding them!")
        __add_half_parsed_goals_events_to_game(game, half_parsed_goals)
    else:
        logger.warning("Half parsed goals + total goals events does not equal to the total score, something wrong, do nothing.")


def __get_player_for_half_parsed_goals_events(game, goal_event):
    """
    Trying to search for exact name, after that for first\last name, after that splitting name by dot (if exist) and search for first\last name.
    """
    # Trying to find player with the exact name.
    name = goal_event['name']
    all_players = game.maccabi_team.players + game.not_maccabi_team.players
    players = [player for player in all_players if player.name == name]
    if players:
        return players[0]

    # Trying to find player with the same first\last name.
    logger.info("Cant find full player name, trying first\last name:{name}".format(name=name))
    players = [player for player in all_players if name in player.name.split()]
    if players:
        return players[0]

    # Trying dot pattern, like : א.זוהר which might be איציק זוהר
    logger.info("Cant find first\last player name, trying check for dot pattern name:{name}".format(name=name))
    if "." in name:
        first, last = [part.strip() for part in name.split(".")]
        players = [player for player in all_players if last in player.name.split()]
        # If we found two players with the same last name, try with the first name.
        if len(players) > 1:
            players = [player for player in players if player.name.startswith(first)]

        if players:
            return players[0]

    return None


def __add_half_parsed_goals_events_to_game(game, half_parsed_goals_events):
    event_to_delete_from_game_half_parsed_event = []

    for event in half_parsed_goals_events:
        if not event['name']:
            logger.warning("Found goal (game date - {date}) with empty player name, skipping".format(date=game.date))
            continue

        player_for_this_event = __get_player_for_half_parsed_goals_events(game, event)
        if player_for_this_event is None:
            logger.warning("Could not find any player that match somehow to this name:{name}, skipping this event".format(name=event['name']))
            continue

        logger.info("Add goal event: {event} to this player:{name} in this game date: {date}"
                    .format(event=event, name=player_for_this_event.name, date=game.date))

        goal_event = GoalGameEvent(event['time_occur'], event['goal_type'])
        player_for_this_event.add_event(goal_event)
        event_to_delete_from_game_half_parsed_event.append(event)

    if event_to_delete_from_game_half_parsed_event:
        logger.info("Removing half parsed goals events from this game")
        new_half_parsed_events = [not_added_half_parsed_event for not_added_half_parsed_event in half_parsed_goals_events if
                                  not_added_half_parsed_event not in event_to_delete_from_game_half_parsed_event]
        game._half_parsed_events = new_half_parsed_events


def __remove_youth_games(maccabi_games_stats):
    # TODO: remove this when we start manipulating youth statistics
    YOUTH_COMPETITIONS = ['גביע המדינה לנוער', 'ליגת העל לנוער']
    logger.info("Removing youth games if exists:(")
    return maccabi_games_stats.create_maccabi_stats_from_games(
        [game for game in maccabi_games_stats.games if game.competition not in YOUTH_COMPETITIONS])


def run_general_fixes(maccabi_games_stats):
    """
    General fixes meant to be stuff like renaming of referees\players names and so on, they are does not depend on the source of maccabi games.
    :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """

    for game in maccabi_games_stats.games:
        __fix_teams_names(game)
        __fix_referees_names(game)
        __fix_competitions_names(game)
        __fix_maccabi_players_names(game)
        __fix_seasons(game)
        __fix_fixtures(game)
        # ATM, only the important events = goals.
        try:
            __fix_half_parsed_goal_events(game)
        except LookupError:
            logger.exception("Error while parsing goals half parsed events.")

    maccabi_games_stats = __remove_youth_games(maccabi_games_stats)

    return maccabi_games_stats
