# -*- coding: utf-8 -*-

from functools import reduce
from collections import Counter

from maccabistats.models.player_game_events import GameEventTypes, GoalTypes


# TODO write wrappers for all

class MaccabiGamesStats(object):

    def __init__(self, maccabi_site_games):
        """
        :type maccabi_site_games: list of maccabistats.models.game_data.GameData
        """

        self.games = maccabi_site_games

    @property
    def home_games(self):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if game.is_maccabi_home_team])

    @property
    def away_games(self):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if not game.is_maccabi_home_team])

    @property
    def available_competitions(self):
        return set(game.competition for game in self.games)

    @property
    def maccabi_wins(self):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if game.is_maccabi_win])

    def get_games_against_team(self, team_name):
        """
        :param team_name: str.
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if team_name == game.not_maccabi_team.name])

    def played_before(self, date):
        return MaccabiGamesStats([game for game in self.games if game.played_before(date)])

    def played_after(self, date):
        """
        :rtype: MaccabiGamesStats
        """
        return MaccabiGamesStats([game for game in self.games if game.played_after(date)])

    def get_games_by_competition(self, competition_type):
        """
        :type competition_type: CompetitionTypes or str
        :rtype: MaccabiGamesStats
        """
        if type(competition_type) is str:
            return MaccabiGamesStats([game for game in self.games if game.competition == competition_type])
        else:
            raise Exception("Enter string or CompetitionType")

    def __get_players_from_all_games_with_most_of_this_condition(self, condition):
        """
        :param condition: this function should get PlayerInGame as param, and return int.
                          0 wont count this player in the final summary.
        :type condition: callable
        :rtype: Counter
        """
        players_with_most_event_type = reduce(
            lambda events_counter_a, events_counter_b: events_counter_a + events_counter_b,

            # TeamInGame saves dict which map between player event to the property
            # which return the most common players which have this event in this game & team.
            [game.maccabi_team.get_players_with_most_of_this_condition(condition)
             for game in self.games])

        # Remove the events by cast player_in_game to 'player' object
        return Counter(
            {player_in_game.get_as_normal_player(): players_with_most_event_type[player_in_game] for player_in_game
             in
             players_with_most_event_type}).most_common()

    @property
    def best_scorers(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_SCORE))

    @property
    def best_scorers_by_freekick(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.FREE_KICK))

    @property
    def best_scorers_by_penalty(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.PENALTY))

    @property
    def best_scorers_by_head(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.HEADER))

    @property
    def best_scorers_by_own_goal(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.goals_count_by_goal_type(GoalTypes.OWN_GOAL))

    @property
    def best_assist(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.GOAL_ASSIST))

    @property
    def most_yellow_carded_players(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.YELLOW_CARD))

    @property
    def most_red_carded_players(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.RED_CARD))

    @property
    def most_substitute_off_players(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.SUBSTITUTION_OUT))

    @property
    def most_substitute_in_players(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.SUBSTITUTION_IN))

    @property
    def most_lineup_players(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.LINE_UP))

    @property
    def most_captains_players(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.CAPTAIN))

    @property
    def most_penalty_missed(self):
        return self.__get_players_from_all_games_with_most_of_this_condition(
            lambda p: p.event_count_by_type(GameEventTypes.PENALTY_MISSED))

    @property
    def most_played_players(self):
        """
        :rtype: Counter
        """
        # Like __get_players_with_most_of_this_event
        most_played_players = reduce(
            lambda played_counter_a, played_counter_b: played_counter_a + played_counter_b,
            [game.maccabi_team.played_players_with_amount
             for game in self.games])

        # Remove the events by cast player_in_game to 'player' object
        return Counter(
            {player_in_game.get_as_normal_player(): most_played_players[player_in_game] for player_in_game
             in
             most_played_players}).most_common()

    @property
    def most_trained_coach(self):
        """
        :rtype: Counter
        """
        return Counter(game.maccabi_team.coach for game in self.games).most_common()

    @property
    def most_winner_coach(self):
        """
        :rtype: Counter
        """
        return Counter(game.maccabi_team.coach for game in self.games if game.is_maccabi_win).most_common()

    @property
    def most_loser_coach(self):
        """
        :rtype: Counter
        """
        return Counter(game.maccabi_team.coach for game in self.games if game.maccabi_score_diff < 0).most_common()

    @property
    def most_winner_coach_by_percentage(self):
        """
        :rtype: Counter
        """

        # Both return as Counter.most_common() which is list (of tuples)
        trained_games = Counter(dict(self.most_trained_coach))
        games_won = Counter(dict(self.most_winner_coach))

        best_coach = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            best_coach[key_name] = round(games_won[coach_name]/trained_times * 100, 2)

        return best_coach.most_common()

    @property
    def most_loser_coach_by_percentage(self):
        """
        :rtype: Counter
        """

        # Both return as Counter.most_common() which is list (of tuples)
        trained_games = Counter(dict(self.most_trained_coach))
        games_lost = Counter(dict(self.most_loser_coach))

        worst_coach = Counter()
        for coach_name, trained_times in trained_games.items():
            key_name = "{coach} - {trained}".format(coach=coach_name, trained=trained_times)
            worst_coach[key_name] = round(games_lost[coach_name] / trained_times * 100, 2)

        return worst_coach.most_common()

    def __len__(self):
        return len(self.games)

    def __getitem__(self, item):
        """
        :rtype: MaccabiSiteGameParser
        """
        return self.games[item]

    def __repr__(self):
        return "Contain {size} games".format(size=len(self))
