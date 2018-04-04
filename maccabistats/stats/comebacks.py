# -*- coding: utf-8 -*-
from maccabistats.models.player_game_events import GoalTypes
import logging

logger = logging.getLogger(__name__)


# This class will handle all comebacks statistics.


class MaccabiGamesComebacksStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.maccabi_games_stats = maccabi_games_stats
        self.games = maccabi_games_stats.games

    def won_from_exactly_one_goal_diff(self):
        return self.won_from_exactly_x_goal_diff(1)

    def won_from_exactly_two_goal_diff(self):
        return self.won_from_exactly_x_goal_diff(2)

    def won_from_exactly_x_goal_diff(self, goals):
        """
        Return Maccabi game stats object(list of games) which maccabi won them after was ahead by x goals (x=goals param).
        :param goals: The number of goals advantage of the opponent.
        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        # Opponent advantage should be negative, positive advantage means maccabi won.
        goals *= -1
        crazy_maccabi_comebacks = []
        for game in self.games:
            if self._max_opponent_goals_advantage(game) == goals and game.is_maccabi_win:
                self._check_for_errors_in_comeback_to_win(game, goals)
                crazy_maccabi_comebacks.append(game)

        return self.maccabi_games_stats.create_maccabi_stats_from_games(crazy_maccabi_comebacks)

    @staticmethod
    def _check_for_errors_in_comeback_to_win(game, goals):
        """
        Check for errors,
         the total score should be at least as twice as the diff +1 (for win).
         the opponent score should be at least the goals diff to check for.
        ATM just write warning if found anything.
        :param game: the game to check errors in.
        :param goals: the goal diff to come from.
        """

        total_score = game.maccabi_team.score + game.not_maccabi_team.score
        if total_score < (2 * (-1) * goals) + 1:
            logger.warning(
                "Found game that his total score {total_score} does not match the conditions (comeback to win)."
                "\ngoal diff: {diff}\n\ngame: {game}".format(total_score=total_score, diff=goals, game=game))
        elif game.not_maccabi_team.score < goals * (-1):
            logger.warning(
                "Found game that his opponent score {opponent_score} does not match the conditions (comeback to win)."
                "\ngoal diff: {diff}\n\ngame: {game}".format(opponent_score=game.not_maccabi_team.score, diff=goals, game=game))

    def tie_from_exactly_one_goal_diff(self):
        return self.tie_from_exactly_x_goal_diff(1)

    def tie_from_exactly_two_goal_diff(self):
        return self.tie_from_exactly_x_goal_diff(2)

    def tie_from_exactly_x_goal_diff(self, goals):
        """
        Return Maccabi game stats object(list of games) which maccabi ends with same score as opponent after was ahead by x goals (x=goals param).
        :param goals: The number of goals advantage of the opponent.
        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        # Opponent advantage should be negative, positive advantage means maccabi won.
        goals *= -1
        crazy_maccabi_comebacks = []
        for game in self.games:
            if self._max_opponent_goals_advantage(game) == goals and game.maccabi_score_diff == 0:
                self._check_for_errors_in_comeback_to_tie(game, goals)
                crazy_maccabi_comebacks.append(game)

        return self.maccabi_games_stats.create_maccabi_stats_from_games(crazy_maccabi_comebacks)

    @staticmethod
    def _check_for_errors_in_comeback_to_tie(game, goals):
        """
        Check for errors,
         the total score should be at least as twice as the diff.
         the opponent score should be at least the goals diff to check for.
        ATM just write warning if found anything.
        :param game: the game to check errors in.
        :param goals: the goal diff to come from.
        """

        total_score = game.maccabi_team.score + game.not_maccabi_team.score
        if total_score < 2 * (-1) * goals:
            logger.warning(
                "Found game that his total score {total_score} does not match the conditions (comeback to tie)."
                "\ngoal diff: {diff}\n\ngame: {game}".format(total_score=total_score, diff=goals, game=game))
        elif game.not_maccabi_team.score < goals * (-1):
            logger.warning(
                "Found game that his opponent score {opponent_score} does not match the conditions (comeback to tie)."
                "\ngoal diff: {diff}\n\ngame: {game}".format(opponent_score=game.not_maccabi_team.score, diff=goals, game=game))

    @staticmethod
    def _max_opponent_goals_advantage(game):
        """
        Calc and return the max goals advantage for maccabi opponent for the given game.
        :rtype: int
        """

        game_goals = game.goals()

        # We save list of all goals timeline and find the minimum (maz advantage for opponent).
        goals_diff = [0]
        for goal in game_goals:
            # TODO remove this shit hardcoded
            if goal['team'] == 'מכבי תל אביב':
                next_goal_status = 1
            else:
                if 'goal_type' in goal and goal['goal_type'] == GoalTypes.OWN_GOAL.value:
                    # The opponent 'scored'
                    next_goal_status = 1
                else:
                    next_goal_status = -1

            # We add the last status + new goal (1 for maccabi, -1 for opponent).
            goals_diff.append(goals_diff[-1] + next_goal_status)

        return min(goals_diff)
