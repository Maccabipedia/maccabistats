import logging
from datetime import timedelta
from itertools import chain

from maccabistats.models.player_game_events import GameEventTypes

logger = logging.getLogger(__name__)
""" This class responsible to find errors in maccabigamesstats object, such as games that the amount of goals does not match to the final score sum,
    empty events and so on.

    This should be run manually.
"""


class ErrorsFinder(object):
    """ Each public function on this class wil lbe run automatically by 'get_all_errors_numbers'. """

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """
        self.maccabi_games_stats = maccabi_games_stats

    def get_games_without_11_players_on_lineup(self):
        """ Each team should has 11 players with lineup event! """

        missing_lineup_games = [game for game in self.maccabi_games_stats
                                if 11 > len(game.not_maccabi_team.lineup_players) or 11 > len(game.maccabi_team.lineup_players)]

        return missing_lineup_games

    def get_lineup_players_with_substitution_in(self):
        """ Players that opened on lineup, should'nt has substitution in event. """

        players = [player for game in self.maccabi_games_stats for player in game.maccabi_team.players + game.not_maccabi_team.players
                   if player.has_event_type(GameEventTypes.LINE_UP) and player.has_event_type(GameEventTypes.SUBSTITUTION_IN)]

        return players

    def get_games_with_missing_goals_events(self):
        """ Total score should be equals to the total goals event """

        games = [game for game in self.maccabi_games_stats if game.maccabi_team.score + game.not_maccabi_team.score != len(game.goals())]

        return games

    def get_games_with_different_score_and_goals(self):
        """ Game score should be equal to the last score at the last goal event.
            Counting only games same goals count and score count (means they wont fail at "get_games_with_missing_goals_events"). """

        games_with_wrong_goals_count = self.get_games_with_missing_goals_events()

        # If the goals count is the same, we can only check for maccabi goals (opponent goals will be equal if maccabi goals is).
        games = [game for game in self.maccabi_games_stats if
                 game not in games_with_wrong_goals_count
                 and (0 if not game.goals() else game.goals()[-1]["maccabi_score"]) != game.maccabi_score]

        return games

    def get_players_with_event_but_without_lineup_or_substitution(self):
        """ Every player that has any event should has atleast lineup or substitution in event """

        players = [player for game in self.maccabi_games_stats for player in game.maccabi_team.players + game.not_maccabi_team.players
                   if len(player.events) > 0 and  # Got any event but no lineup or subs in
                   not player.has_event_type(GameEventTypes.LINE_UP) and not player.has_event_type(GameEventTypes.SUBSTITUTION_IN)]
        return players

    def get_goals_scored_at_minute_zero(self):
        zero_time = str(timedelta(0))
        all_goals = list(chain.from_iterable([game.goals() for game in self.maccabi_games_stats]))
        return list(filter(lambda g: g['time_occur'] == zero_time, all_goals))

    def get_all_errors_numbers(self):
        """ Iterate over all this class functions without this one, and summarize the results. """
        errors_finders = [func for func in dir(self) if
                          callable(getattr(self, func)) and func != "get_all_errors_numbers" and not func.startswith("_")]

        for func_name in errors_finders:
            error_finder_func = getattr(self, func_name)
            logger.info("{func_name}: returned {count} items".format(func_name=func_name,
                                                                     count=len(error_finder_func())))
