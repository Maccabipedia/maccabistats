# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

# This class will handle all coaches statistics.
from typing import Tuple, List


class MaccabiGamesCoachesStats(object):

    def __init__(self, maccabi_games_stats):
        """
        :type maccabi_games_stats: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """

        self.games = maccabi_games_stats.games
        
    @property
    def most_clean_sheet_games_coach(self) -> List[Tuple[str, int]]:
        return Counter(game.maccabi_team.coach for game in self.games if game.not_maccabi_team.score == 0).most_common()

    @property
    def most_goals_for_maccabi_coach(self) -> List[Tuple[str, int]]:
        coach_to_goals = defaultdict(lambda: 0)
        for game in self.games:
            coach_to_goals[game.maccabi_team.coach] += game.maccabi_team.score

        return Counter(coach_to_goals).most_common()

    @property
    def most_goals_against_maccabi_coach(self) -> List[Tuple[str, int]]:
        coach_to_goals = defaultdict(lambda: 0)
        for game in self.games:
            coach_to_goals[game.maccabi_team.coach] += game.not_maccabi_team.score

        return Counter(coach_to_goals).most_common()

    @property
    def most_trained_coach(self) -> List[Tuple[str, int]]:
        return Counter(game.maccabi_team.coach for game in self.games).most_common()

    @property
    def most_winner_coach(self) -> List[Tuple[str, int]]:
        return Counter(game.maccabi_team.coach for game in self.games if game.is_maccabi_win).most_common()

    @property
    def most_loser_coach(self) -> List[Tuple[str, int]]:
        return Counter(game.maccabi_team.coach for game in self.games if game.maccabi_score_diff < 0).most_common()

    @property
    def most_winner_coach_by_percentage(self) -> List[Tuple[str, int]]:
        # Both return as Counter.most_common() which is list (of tuples)
        trained_games = Counter(dict(self.most_trained_coach))
        games_won = Counter(dict(self.most_winner_coach))

        best_coach = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            best_coach[key_name] = round(games_won[coach_name] / trained_times * 100, 2)

        return best_coach.most_common()

    @property
    def most_loser_coach_by_percentage(self) -> List[Tuple[str, int]]:
        # Both return as Counter.most_common() which is list (of tuples)
        trained_games = Counter(dict(self.most_trained_coach))
        games_lost = Counter(dict(self.most_loser_coach))

        worst_coach = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            worst_coach[key_name] = round(games_lost[coach_name] / trained_times * 100, 2)

        return worst_coach.most_common()

    @property
    def most_clean_sheet_games_coach_by_percentage(self) -> List[Tuple[str, int]]:
        # Both return as Counter.most_common() which is list (of tuples)
        trained_games = Counter(dict(self.most_trained_coach))
        clean_sheet_games = Counter(dict(self.most_clean_sheet_games_coach))

        coaches = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            coaches[key_name] = round(clean_sheet_games[coach_name] / trained_times * 100, 2)

        return coaches.most_common()

    @property
    def most_goals_for_maccabi_per_game_coach(self):
        trained_games = Counter(dict(self.most_trained_coach))
        goals_for_coach = Counter(dict(self.most_goals_for_maccabi_coach))

        coaches = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            coaches[key_name] = round(goals_for_coach[coach_name] / trained_times, 2)

        return coaches.most_common()

    @property
    def most_goals_against_maccabi_per_game_coach(self):
        trained_games = Counter(dict(self.most_trained_coach))
        goals_for_coach = Counter(dict(self.most_goals_against_maccabi_coach))

        coaches = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            coaches[key_name] = round(goals_for_coach[coach_name] / trained_times, 2)

        return coaches.most_common()