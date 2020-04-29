# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict

from maccabistats.stats.players_games_condition import PlayerGameMatcher, PlayerGamesCondition

logger = logging.getLogger(__name__)


class MaccabiGamesPlayersFirstAndLastGamesStats(object):
    """
    This class will handle the players first and last games they participate in and check whether a condition satisfy in that game.
    For example, "Who are the players that score in their first game"?

    Dont be confused with 'MaccabiGamesPlayersSpecialGamesStats' which checks:
    WHEN every player did an event at the first time, like:
    "When every player scored his first goal?"

    """

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """
        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def _players_that_satisfy_condition_at_their_first_or_last_game(self, player_game_condition, player_game_to_search_for):
        """
        Check which players satisfy the given condition at their first or last game, like "which players score at their first game?"

        :param player_game_condition: A function that will search for a game, gets (game, player_name) --> bool
        :type player_game_condition: callable
        :param player_game_to_search_for: Whether to search for the players first game or last game that satisfy the condition
        :type player_game_to_search_for: PlayerGameMatcher
        :return: The players that satisfy the condition at their first game + the first game, ordered by the game data ASC
        :rtype: dict[str, maccabistats.models.game_data.GameData]
        """
        games_by_player_name = self.maccabi_games_stats.games_by_player_name()
        players_that_satisfy_condition = dict()

        for player_name, player_games in games_by_player_name.items():
            if player_game_to_search_for.value == PlayerGameMatcher.LAST_GAME.value:
                game_to_check = player_games[-1]
            elif player_game_to_search_for.value == PlayerGameMatcher.FIRST_GAME.value:
                game_to_check = player_games[0]
            else:
                raise TypeError("Unknown game matcher")

            if player_game_condition(game_to_check, player_name):
                players_that_satisfy_condition[player_name] = game_to_check

        return OrderedDict(sorted(players_that_satisfy_condition.items(), key=lambda item: item[1].date))

    def players_that_scored_at_their_first_game(self, score_at_least=1):
        return self._players_that_satisfy_condition_at_their_first_or_last_game(
            PlayerGamesCondition.create_score_x_goals_in_game__condition(score_at_least), PlayerGameMatcher.FIRST_GAME)

    def players_that_scored_at_their_last_game(self, score_at_least=1):
        return self._players_that_satisfy_condition_at_their_first_or_last_game(
            PlayerGamesCondition.create_score_x_goals_in_game__condition(score_at_least), PlayerGameMatcher.LAST_GAME)

    def players_that_assisted_at_their_first_game(self, assist_at_least=1):
        return self._players_that_satisfy_condition_at_their_first_or_last_game(
            PlayerGamesCondition.create_assist_x_goals_in_game__condition(assist_at_least), PlayerGameMatcher.FIRST_GAME)

    def players_that_assisted_at_their_last_game(self, assist_at_least=1):
        return self._players_that_satisfy_condition_at_their_first_or_last_game(
            PlayerGamesCondition.create_assist_x_goals_in_game__condition(assist_at_least), PlayerGameMatcher.LAST_GAME)
