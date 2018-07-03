from maccabistats.models.player_game_events import GoalTypes, GameEvent, GameEventTypes
from datetime import timedelta, datetime
from dateutil.parser import parse as datetime_parser

import logging

logger = logging.getLogger(__name__)

_games_dates_to_change = [("2012-03-23", "2012-03-24"),  # Against Hapoel Tel aviv
                          ("2012-01-31", "2012-01-30"),  # Against Kiryat Shmona
                          ("2011-02-17", "2011-02-19"),  # Against Hapoel PT
                          ]


def __fix_games_date(maccabi_games_stats):
    for game_dates in _games_dates_to_change:
        matching_games = maccabi_games_stats.played_at(game_dates[0])
        if not matching_games:
            logger.warning(f"Cant find game's original date so it may be changed: {game_dates[0]} (should be {game_dates[1]}), Skipping this game.")
            continue
        elif len(matching_games) != 1:
            logger.warning(f"Found ({len(matching_games)}) games from this date: {game_dates[0]} (should be {game_dates[1]}), Skipping this game.")
            continue

        game_to_be_changed = matching_games[0]
        game_to_be_changed.date = datetime_parser(game_dates[1])
        logger.info(f"Changed game date from {game_dates[0]} -> {game_dates[1]}.")


def __fix_basel_three_three(games):
    against_basel_tie_three = games.get_games_against_team("באזל").played_after("2013-08-06").played_before("2013-08-06")
    against_basel_tie_three = against_basel_tie_three[0]
    if against_basel_tie_three.not_maccabi_team.scored_players[0].events[2].goal_type is not GoalTypes.OWN_GOAL:
        against_basel_tie_three.not_maccabi_team.scored_players[0].events[2].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed פביאן שאר goal to be own goal at min 34.")


def __fix_haifa_three_one(games):
    against_haifa_three_one_win = games.get_games_against_team("מכבי חיפה").played_after("2014-10-20").played_before("2014-10-20")
    against_haifa_three_one_win = against_haifa_three_one_win[0]
    if against_haifa_three_one_win.not_maccabi_team.scored_players[0].events[1].goal_type is not GoalTypes.OWN_GOAL:
        against_haifa_three_one_win.not_maccabi_team.scored_players[0].events[1].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed טאלב טאווטחה goal to be own goal at min 52.")


def __fix_hibernians_five_one(games):
    against_hibernians_five_one_win = games.get_games_against_team("היברניאנס").played_after("2015-07-21").played_before("2015-07-21")
    against_hibernians_five_one_win = against_hibernians_five_one_win[0]
    if against_hibernians_five_one_win.not_maccabi_team.scored_players[1].events[1].goal_type is not GoalTypes.OWN_GOAL:
        against_hibernians_five_one_win.not_maccabi_team.scored_players[1].events[1].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed ג'ורג' פריירה goal to be own goal at min 52.")


def __fix_akko_two_zero(games):
    against_akko_two_zero_win = games.get_games_against_team("הפועל עכו").played_after("2012-10-20").played_before("2012-10-20")
    against_akko_two_zero_win = against_akko_two_zero_win[0]
    if against_akko_two_zero_win.not_maccabi_team.scored_players[0].events[1].goal_type is not GoalTypes.OWN_GOAL:
        against_akko_two_zero_win.not_maccabi_team.scored_players[0].events[1].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed אימורו לוקמן goal to be own goal at min 52.")


def __fix_beitar_three_two(games):
    against_beitar_three_two_win = games.get_games_against_team('בית"ר ירושלים').played_after("2003-05-17").played_before("2003-05-17")
    against_beitar_three_two_win = against_beitar_three_two_win[0]
    david = [p for p in against_beitar_three_two_win.not_maccabi_team.players if p.name == "דוד אמסלם"][0]
    if not david.scored:
        goal = GameEvent(GameEventTypes.GOAL_SCORE, timedelta(minutes=33))
        david.add_event(goal)
        logger.info("Fixed דוד אמסלם goal - probably does not exists after crawling maccabi-tlv site( appear in events page but not in squads page.")

    if against_beitar_three_two_win._half_parsed_events:
        logger.info("Removing half parsed goals events from this game ({date}".format(date=against_beitar_three_two_win.date))
        against_beitar_three_two_win._half_parsed_events = list(
            filter(lambda event: event['event_type'] != GameEventTypes.GOAL_SCORE, against_beitar_three_two_win._half_parsed_events))


def __fix_hapoel_haifa_four_two_date_99_00(games):
    # This game saved on maccabi-tlv site as against maccabi-haifa, that mistake, it should be against hapoel-haifa, round 18 for this season.
    # The original date is: 2000-01-03 (yy-mm-dd).
    against_hapoel_haifa = games.played_at("2000-03-01")
    if len(against_hapoel_haifa) > 1:
        logger.warning("Found more than one game that should be fixed at date : 2000-03-01, Taking the first.")

    against_hapoel_haifa = against_hapoel_haifa[0]
    against_hapoel_haifa.not_maccabi_team.name = "הפועל חיפה"
    against_hapoel_haifa.date = datetime(year=2000, month=1, day=3)
    logger.info("Changed the game at data: 2000-03-01 to be at date: 2000-01-03 and replaced the opponent name from הפועל חיפה to מכבי חיפה")


def fix_specific_games(games):
    # TODO separate to two diff function (or any another logic).

    # Fix goals:
    __fix_basel_three_three(games)
    __fix_haifa_three_one(games)
    __fix_hibernians_five_one(games)
    __fix_akko_two_zero(games)
    __fix_beitar_three_two(games)

    # Fix dates & name:
    __fix_hapoel_haifa_four_two_date_99_00(games)

    # Fix just dates:
    __fix_games_date(games)

    return games
