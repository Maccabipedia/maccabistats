from maccabistats.models.player_game_events import GoalTypes, GameEvent, GameEventTypes
from datetime import timedelta

import logging

logger = logging.getLogger(__name__)


def __fix_basel_three_three(games):
    against_basel_tie_three = games.get_games_against_team("באזל").played_after("06.08.2013").played_before("06.08.2013")
    against_basel_tie_three = against_basel_tie_three[0]
    if against_basel_tie_three.not_maccabi_team.scored_players[0].events[2].goal_type is not GoalTypes.OWN_GOAL:
        against_basel_tie_three.not_maccabi_team.scored_players[0].events[2].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed פביאן שאר goal to be own goal at min 34.")


def __fix_haifa_three_one(games):
    against_haifa_three_one_win = games.get_games_against_team("מכבי חיפה").played_after("20.10.2014").played_before("20.10.2014")
    against_haifa_three_one_win = against_haifa_three_one_win[0]
    if against_haifa_three_one_win.not_maccabi_team.scored_players[0].events[1].goal_type is not GoalTypes.OWN_GOAL:
        against_haifa_three_one_win.not_maccabi_team.scored_players[0].events[1].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed טאלב טאווטחה goal to be own goal at min 52.")


def __fix_hibernians_five_one(games):
    against_hibernians_five_one_win = games.get_games_against_team("היברניאנס").played_after("21.07.2015").played_before("21.07.2015")
    against_hibernians_five_one_win = against_hibernians_five_one_win[0]
    if against_hibernians_five_one_win.not_maccabi_team.scored_players[1].events[1].goal_type is not GoalTypes.OWN_GOAL:
        against_hibernians_five_one_win.not_maccabi_team.scored_players[1].events[1].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed ג'ורג' פריירה goal to be own goal at min 52.")


def __fix_akko_two_zero(games):
    against_akko_two_zero_win = games.get_games_against_team("הפועל עכו").played_after("20.10.2012").played_before("20.10.2012")
    against_akko_two_zero_win = against_akko_two_zero_win[0]
    if against_akko_two_zero_win.not_maccabi_team.scored_players[0].events[1].goal_type is not GoalTypes.OWN_GOAL:
        against_akko_two_zero_win.not_maccabi_team.scored_players[0].events[1].goal_type = GoalTypes.OWN_GOAL
        logger.info("Fixed אימורו לוקמן goal to be own goal at min 52.")


def __fix_beitar_three_two(games):
    against_beitar_three_two_win = games.get_games_against_team('בית"ר ירושלים').played_after("17.05.2003").played_before("17.05.2003")
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


def fix_specific_games(games):
    __fix_basel_three_three(games)
    __fix_haifa_three_one(games)
    __fix_hibernians_five_one(games)
    __fix_akko_two_zero(games)
    __fix_beitar_three_two(games)
