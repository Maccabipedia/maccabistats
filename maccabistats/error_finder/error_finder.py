import logging
from collections import defaultdict
from datetime import timedelta
from itertools import chain

from maccabistats.models.player_game_events import GameEventTypes
from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats

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

    def get_games_without_11_maccabi_players_on_lineup(self):
        """ Each team should has 11 players with lineup event! but we care more about maccabi"""

        missing_lineup_games = [game for game in self.maccabi_games_stats
                                if 11 != len(game.maccabi_team.lineup_players)]

        return MaccabiGamesStats(missing_lineup_games)

    def get_lineup_players_with_substitution_in(self):
        """ Players that opened on lineup, should'nt has substitution in event. """

        players_with_games = [(player, game) for game in self.maccabi_games_stats for player in
                              game.maccabi_team.players + game.not_maccabi_team.players
                              if player.has_event_type(GameEventTypes.LINE_UP) and player.has_event_type(GameEventTypes.SUBSTITUTION_IN)]

        return players_with_games

    def get_games_with_missing_goals_events(self):
        """ Total score should be equals to the total goals event, excluding games that were finished by technical result """

        games = [game for game in self.maccabi_games_stats
                 if (game.maccabi_team.score + game.not_maccabi_team.score != len(game.goals())) and not game.technical_result]

        return MaccabiGamesStats(games)

    def get_games_with_different_score_and_goals(self):
        """ Game score should be equal to the last score at the last goal event.
            Counting only games same goals count and score count (means they wont fail at "get_games_with_missing_goals_events"). """

        games_with_wrong_goals_count = self.get_games_with_missing_goals_events()

        # If the goals count is the same, we can only check for maccabi goals (opponent goals will be equal if maccabi goals is).
        games = [game for game in self.maccabi_games_stats if
                 game not in games_with_wrong_goals_count
                 and (0 if not game.goals() else game.goals()[-1]["maccabi_score"]) != game.maccabi_score]

        return MaccabiGamesStats(games)

    def get_players_with_event_but_without_lineup_or_substitution(self):
        """ Every player that has any event should has atleast lineup or substitution or bench in event """

        players_with_games = [(player, game) for game in self.maccabi_games_stats for player in
                              game.maccabi_team.players + game.not_maccabi_team.players
                              if len(player.events) > 0 and  # Got any event but no lineup or subs in
                              not player.has_event_type(GameEventTypes.LINE_UP) and not player.has_event_type(GameEventTypes.SUBSTITUTION_IN)
                              and not player.has_event_type(GameEventTypes.BENCHED)]
        return players_with_games

    def get_goals_scored_at_minute_zero(self):
        zero_time = str(timedelta(0))
        all_goals = list(chain.from_iterable([game.goals() for game in self.maccabi_games_stats]))
        return list(filter(lambda g: g['time_occur'] == zero_time, all_goals))

    def get_games_with_incorrect_season(self):
        """ Finds games which their date does not match the seasons (date between seasons). """

        def validate_season(game):
            if game.season[-2:] == "00":  # We should add 100 year to the max season in this counting system:
                return int(game.season[:4]) <= game.date.year <= int(game.season[:2] + game.season[-2:]) + 100
            else:
                return int(game.season[:4]) <= game.date.year <= int(game.season[:2] + game.season[-2:])

        games_with_incorrect_season = [(game.season, str(game.date), game) for game in self.maccabi_games_stats if not validate_season(game)]

        return games_with_incorrect_season

    def get_players_with_unknown_events(self):
        players_with_unknown_events = [(player, game) for game in self.maccabi_games_stats for player in
                                       game.maccabi_team.players + game.not_maccabi_team.players if player.has_event_type(GameEventTypes.UNKNOWN)]
        return players_with_unknown_events

    def get_missing_league_games_fixtures(self):
        """
        For each season get the max fixture number and check whether the len of this season games equal to it
        """

        missing_fixtures_from_all_seasons = []

        seasons = self.maccabi_games_stats.league_games.seasons.get_seasons_stats()
        for season in seasons:
            current_season_fixtures = [game.league_fixture for game in season if game.league_fixture]
            if not current_season_fixtures:  # If we are dealing with no league games in this season
                continue

            should_be_fixtures = set(range(1, max(current_season_fixtures) + 1))
            missing_fixtures = should_be_fixtures.difference(current_season_fixtures)

            if missing_fixtures:
                [missing_fixtures_from_all_seasons.append((season[0].season, missing_fixture)) for missing_fixture in missing_fixtures]

        return missing_fixtures_from_all_seasons

    def get_double_league_games_fixtures(self):
        """
        For each season check whether we have double fixtures (numbers)
        """

        fixtures_from_all_seasons = defaultdict(list)

        seasons = self.maccabi_games_stats.league_games.seasons.get_seasons_stats()
        for season in seasons:
            if season:  # Any games at this season
                for game in season:
                    fixtures_from_all_seasons[f"season {season[0].season} fixture {game.league_fixture}"].append(game)

        double_fixtures = [(season_and_fixture, MaccabiGamesStats(games)) for season_and_fixture, games in fixtures_from_all_seasons.items() if
                           len(games) > 1]
        return double_fixtures

    def get_games_without_stadium(self):
        """
        Returns the games without defined stadium
        """

        return [game for game in self.maccabi_games_stats.games if not game.stadium]

    def get_games_without_referee(self):
        """
        Returns the games without defined referee
        """

        return [game for game in self.maccabi_games_stats.games if not game.referee]

    def get_players_which_play_more_than_x_years(self, number_of_years=25):
        """
        Returns the players who play more than the given years, default 25 years.
        This may indicate on naming errors
        :type number_of_years: int
        :return: Player name and his games
        :rtype: str, maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        players_who_played_too_much = []
        for player_name in self.maccabi_games_stats.available_players_names:
            player_games = self.maccabi_games_stats.get_games_with_player_name(player_name)
            if player_games[-1].date - player_games[0].date > timedelta(days=365 * number_of_years):
                players_who_played_too_much.append((player_name, player_games))

        return players_who_played_too_much

    def get_all_errors_numbers(self):
        """ Iterate over all this class functions without this one, and summarize the results. """
        errors_finders = [func for func in dir(self) if
                          callable(getattr(self, func)) and func != "get_all_errors_numbers" and not func.startswith("_")]

        for func_name in errors_finders:
            error_finder_func = getattr(self, func_name)
            logger.info("{func_name}: returned {count} items".format(func_name=func_name,
                                                                     count=len(error_finder_func())))
