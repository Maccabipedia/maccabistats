from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING, Callable, Tuple, List, Dict

from progressbar import ProgressBar

from maccabistats.models.game_data import GameData

if TYPE_CHECKING:
    from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats

    PlayerAndGames = Tuple[str, MaccabiGamesStats]

logger = logging.getLogger(__name__)




class MaccabiGamesPlayersStreaksStats(object):
    """
    This class will handle all players streaks statistics.
    """

    def __init__(self, maccabi_games_stats: MaccabiGamesStats):
        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def _get_players_streak_by_condition(self,
                                         streak_condition: Callable[[MaccabiGamesStats, str], int],
                                         top_players_count: int = 10) -> List[PlayerAndGames]:
        """
        For each player, given his MaccabiGamesStats - calculate the relevant streak.
        For example: "streak_condition= lambda games, player_name: games.streaks.get_longest_unbeaten_streak_games())"

        :param streak_condition: callable that get (MaccabiGamesStats, player_name) as params and return streak
        """

        pbar = ProgressBar()
        players_games = defaultdict(list)

        for game in pbar(self.games):
            for player in game.maccabi_team.played_players:
                players_games[player.name].append(game)

        player_maccabi_stats: Dict[str, MaccabiGamesStats] = dict()

        for player in self.maccabi_games_stats.available_players:
            player_maccabi_stats[player.name] = self.maccabi_games_stats.create_maccabi_stats_from_games(
                players_games[player.name])

        unsorted_players_streaks = {player.name: streak_condition(player_maccabi_stats[player.name], player.name) for
                                    player in self.maccabi_games_stats.available_players}

        return sorted(unsorted_players_streaks.items(), key=lambda kv: len(kv[1]), reverse=True)[:top_players_count]

    def _get_players_streak_by_condition_from_all_games(self,
                                                        streak_condition: Callable[[MaccabiGamesStats, str], int],
                                                        top_players_count: int = 10) -> List[PlayerAndGames]:
        """
        Same as "_get_players_streak_by_condition", but we don't filters the games for each player.
        In this function the condition is check against all of the available games,
        even if the player didn't play in a game
        (useful for queries like "which player played the most games in a row?").
        """
        pbar = ProgressBar()
        unsorted_players_streaks = dict()
        for player in pbar(self.maccabi_games_stats.available_players):
            unsorted_players_streaks[player.name] = streak_condition(self.maccabi_games_stats, player.name)

        return sorted(unsorted_players_streaks.items(), key=lambda kv: len(kv[1]), reverse=True)[:top_players_count]

    # region Top players streaks

    def get_players_with_best_unbeaten_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_unbeaten_streak_games())

    def get_players_with_best_win_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_wins_streak_games())

    def get_players_with_best_ties_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_ties_streak_games())

    def get_players_with_best_losses_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_losses_streak_games())

    def get_players_with_best_maccabi_score_goal_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_score_at_least_games(1))

    def get_players_with_best_maccabi_score_at_least_goals_streak(self, goals_amount: int) -> List[PlayerAndGames]:
        """
        :param goals_amount: Goals amount that maccabi scored (at least)
        """
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_score_at_least_games(goals_amount))

    def get_players_with_best_maccabi_score_no_goal_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_score_exactly_games(0))

    def get_players_with_best_maccabi_score_exactly_goals_streak(self, goals_amount: int) -> List[PlayerAndGames]:
        """
        :param goals_amount: Goals amount that maccabi scored (exactly)
        """
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_score_exactly_games(goals_amount))

    def get_players_with_best_clean_sheets_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_clean_sheet_games())

    def get_players_with_best_played_in_game_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition_from_all_games(
            lambda games, player_name: games.streaks.get_longest_player_played_in_game(player_name))

    def _find_player_goal_scoring_best_streak(self, player_name: str) -> List[PlayerAndGames]:
        """
         DO NOT use get_games_by_played_player_name, uses existing games
        """

        def player_scored_in_game(game: GameData):
            players_who_scored = [player.name for player in game.maccabi_team.scored_players]
            return player_name in players_who_scored

        return self.maccabi_games_stats.streaks._get_longest_streak_by_condition(player_scored_in_game)

    def get_players_with_best_goal_scoring_streak(self):
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.players_streaks._find_player_goal_scoring_best_streak(player_name))

    def _find_player_goal_assisting_best_streak(self, player_name: str) -> List[PlayerAndGames]:
        """
         DO NOT use get_games_by_played_player_name, uses existing games
        """

        def player_assist_in_game(game: GameData):
            players_who_assisted = [player.name for player in game.maccabi_team.assist_players]
            return player_name in players_who_assisted

        return self.maccabi_games_stats.streaks._get_longest_streak_by_condition(player_assist_in_game)

    def get_players_with_best_goal_assisting_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.players_streaks._find_player_goal_assisting_best_streak(player_name))

    def _find_player_goal_involving_best_streak(self, player_name: str):
        """
         DO NOT use get_games_by_played_player_name, uses existing games
        """

        def player_involved_in_goal_in_game(game: GameData):
            players_who_involved = [player.name for player in game.maccabi_team.scored_players]
            players_who_involved.extend([player.name for player in game.maccabi_team.assist_players])
            return player_name in players_who_involved

        return self.maccabi_games_stats.streaks._get_longest_streak_by_condition(player_involved_in_goal_in_game)

    def get_players_with_best_goal_involving_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.players_streaks._find_player_goal_involving_best_streak(player_name))

    def get_players_with_current_unbeaten_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_unbeaten_streak())

    # endregion

    # region Current streaks for players

    def get_players_with_best_scored_against_maccabi_not_more_than_streak(self, not_maccabi_score: int) \
            -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_longest_scored_against_maccabi_not_more_than_games(
                not_maccabi_score))

    def get_players_with_current_win_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(lambda games, player_name: games.streaks.get_current_wins_streak())

    def get_players_with_current_ties_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(lambda games, player_name: games.streaks.get_current_ties_streak())

    def get_players_with_current_losses_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_losses_streak())

    def get_players_with_current_maccabi_score_goal_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_score_at_least_streak(1))

    def get_players_with_current_maccabi_score_at_least_goals_streak(self, goals_amount: int) -> List[PlayerAndGames]:
        """
        :param goals_amount: Goals amount that maccabi scored (at least)
        """

        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_score_at_least_streak(goals_amount))

    def get_players_with_current_maccabi_score_no_goal_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_score_exactly_streak(0))

    def get_players_with_current_maccabi_score_exactly_goals_streak(self, goals_amount: int) -> List[PlayerAndGames]:
        """
        :param goals_amount: Goals amount that maccabi scored (exactly)
        """

        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_score_exactly_streak(goals_amount))

    def get_players_with_current_clean_sheets_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_clean_sheet_streak())

    def _find_player_goal_scoring_current_streak(self, player_name: str) -> List[PlayerAndGames]:
        """
        DO NOT use get_games_by_played_player_name, uses existing games
        """

        def player_scored_in_game(game):
            players_who_scored = [player.name for player in game.maccabi_team.scored_players]
            return player_name in players_who_scored

        return self.maccabi_games_stats.streaks._get_current_streak_by_condition(player_scored_in_game)

    def get_players_with_current_goal_scoring_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.players_streaks._find_player_goal_scoring_current_streak(player_name))

    def _find_player_goal_assisting_current_streak(self, player_name: str) -> List[PlayerAndGames]:
        """
        DO NOT use get_games_by_played_player_name, uses existing games
        """

        def player_assist_in_game(game):
            players_who_assisted = [player.name for player in game.maccabi_team.assist_players]
            return player_name in players_who_assisted

        return self.maccabi_games_stats.streaks._get_current_streak_by_condition(player_assist_in_game)

    def get_players_with_current_goal_assisting_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.players_streaks._find_player_goal_assisting_current_streak(player_name))

    def _find_player_goal_involving_current_streak(self, player_name: str) -> List[PlayerAndGames]:
        """
        DO NOT use get_games_by_played_player_name, uses existing games
        """

        def player_involved_in_goal_in_game(game):
            players_who_involved = [player.name for player in game.maccabi_team.scored_players]
            players_who_involved.extend([player.name for player in game.maccabi_team.assist_players])
            return player_name in players_who_involved

        return self.maccabi_games_stats.streaks._get_current_streak_by_condition(player_involved_in_goal_in_game)

    def get_players_with_current_goal_involving_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.players_streaks._find_player_goal_involving_current_streak(player_name))

    def get_players_with_current_scored_against_maccabi_not_more_than_streak(self, not_maccabi_score: int) \
            -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition(
            lambda games, player_name: games.streaks.get_current_scored_against_maccabi_not_more_than_streak(
                not_maccabi_score))

    def get_players_with_current_played_in_game_streak(self) -> List[PlayerAndGames]:
        return self._get_players_streak_by_condition_from_all_games(
            lambda games, player_name: games.streaks.get_current_player_played_in_game_streak(player_name))

    # endregion
