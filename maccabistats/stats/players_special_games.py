# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from enum import Enum

from maccabistats.maccabipedia.players import MaccabiPediaPlayers

logger = logging.getLogger(__name__)


class PlayerAging(Enum):
    YOUNGEST_PLAYERS = "youngest"
    OLDEST_PLAYERS = "oldest"


class PlayerGameMatcher(Enum):
    FIRST_GAME = "first_game"
    LAST_GAME = "last_game"


class PlayerAgeAtSpecialGame(object):
    _days_in_year = 365.2425

    def __init__(self, player_name, player_birth_date, special_game):
        """
        :type player_name: str
        :type player_birth_date: datetime.datetime
        :type special_game: maccabistats.models.game_data.GameData
        """
        self.player_name = player_name
        self.birth_date = player_birth_date
        self.first_game = special_game

        self.time_in_days = special_game.date - player_birth_date
        self.time_in_years = self.time_in_days / timedelta(self._days_in_year)

    def __repr__(self):
        return f"{self.player_name} | {self.time_in_years:.2f} שנים --> המשחק: {self.first_game.date.date()} (נולד ב {self.birth_date.date()})"


class PlayerGamesCondition(object):

    @staticmethod
    def play_in_game(game, player_name):
        return player_name in [p.name for p in game.maccabi_team.played_players]

    @staticmethod
    def create_score_x_goals_in_game__condition(goals_at_least):
        def score_in_game_x_goals(game, player_name):
            return game.maccabi_team.scored_players_with_amount.get(player_name, 0) >= goals_at_least

        return score_in_game_x_goals

    @staticmethod
    def create_assist_x_goals_in_game__condition(assist_at_least):
        def assist_in_game(game, player_name):
            return game.maccabi_team.assist_players_with_amount.get(player_name, 0) >= assist_at_least

        return assist_in_game


class MaccabiGamesPlayersSpecialGamesStats(object):
    """
    This class will handle all players events and the first time they occur, like: first time that a player score - whos the youngest?
    """

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """
        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games
        self.players_birth_dates = MaccabiPediaPlayers.get_players_data().players_dates

    def _players_by_game_condition_ordered_by_age(self, player_game_condition, player_game_to_search_for, order_by_age_option, players_count):
        """
        :param player_game_condition: A function that will search for a game, gets (game, player_name) --> bool
        :type player_game_condition: callable
        :param player_game_to_search_for: Whether to search for the players first game or last game that satisfy the condition
        :type player_game_to_search_for: PlayerGameMatcher
        :param order_by_age_option: Do we want the youngest or oldest players?
        :type order_by_age_option: PlayerAging
        :param: The amount of players we want to return
        :type players_count: int
        :return: The players that satisfy the player game condition, from youngest and above
        :rtype: list of PlayerAgeAtSpecialGame
        """
        games_by_player_name = self.maccabi_games_stats.games_by_player_name()

        first_game_by_player_name = dict()
        for player_name, player_games in games_by_player_name.items():
            if player_game_to_search_for.value == PlayerGameMatcher.LAST_GAME.value:
                player_games = reversed(player_games)  # We should search for the player last game

            first_game = next((game for game in player_games if player_game_condition(game, player_name)), None)
            if first_game is None:
                continue  # This player does not satisfy the condition
            if MaccabiPediaPlayers.missing_birth_date_value == self.players_birth_dates[player_name]:
                continue  # This player does not have any birth date on our db

            first_game_by_player_name[player_name] = PlayerAgeAtSpecialGame(player_name, self.players_birth_dates[player_name], first_game)

        players_by_age = sorted(first_game_by_player_name.values(), key=lambda player_first_game: player_first_game.time_in_days)
        if order_by_age_option.value == PlayerAging.OLDEST_PLAYERS.value:
            players_by_age = list(reversed(players_by_age))

        return players_by_age[:players_count]

    def youngest_players_by_first_time_to_play(self, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.play_in_game,
                                                              PlayerGameMatcher.FIRST_GAME, PlayerAging.YOUNGEST_PLAYERS, players_count)

    def oldest_players_by_first_time_to_play(self, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.play_in_game,
                                                              PlayerGameMatcher.FIRST_GAME, PlayerAging.OLDEST_PLAYERS, players_count)

    def oldest_players_by_last_time_to_play(self, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.play_in_game,
                                                              PlayerGameMatcher.LAST_GAME, PlayerAging.OLDEST_PLAYERS, players_count)

    def youngest_players_by_first_time_to_score(self, score_at_least=1, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.create_score_x_goals_in_game__condition(score_at_least),
                                                              PlayerGameMatcher.FIRST_GAME, PlayerAging.YOUNGEST_PLAYERS, players_count)

    def oldest_players_by_first_time_to_score(self, score_at_least=1, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.create_score_x_goals_in_game__condition(score_at_least),
                                                              PlayerGameMatcher.FIRST_GAME, PlayerAging.OLDEST_PLAYERS, players_count)

    def oldest_players_by_last_time_to_score(self, score_at_least=1, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.create_score_x_goals_in_game__condition(score_at_least),
                                                              PlayerGameMatcher.LAST_GAME, PlayerAging.OLDEST_PLAYERS, players_count)

    def youngest_players_by_first_time_to_assist(self, assist_at_least=1, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.create_assist_x_goals_in_game__condition(assist_at_least),
                                                              PlayerGameMatcher.FIRST_GAME, PlayerAging.YOUNGEST_PLAYERS, players_count)

    def oldest_players_by_first_time_to_assist(self, assist_at_least=1, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.create_assist_x_goals_in_game__condition(assist_at_least),
                                                              PlayerGameMatcher.FIRST_GAME, PlayerAging.OLDEST_PLAYERS, players_count)

    def oldest_players_by_last_time_to_assist(self, assist_at_least=1, players_count=50):
        return self._players_by_game_condition_ordered_by_age(PlayerGamesCondition.create_assist_x_goals_in_game__condition(assist_at_least),
                                                              PlayerGameMatcher.LAST_GAME, PlayerAging.OLDEST_PLAYERS, players_count)