#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import reduce
from collections import Counter

from maccabi_stats.models.player_game_events import GameEventTypes
from maccabi_stats.parse.maccabi_tlv_site.game_parser import MaccabiSiteGameParser
from maccabi_stats.models.competition_types import CompetitionTypes


# TODO write wrappers for all

class MaccabiSiteGamesWrapper(object):

    def __init__(self, maccabi_site_games):
        """
        :type maccabi_site_games: list of MaccabiSiteGameParser
        """

        self.games = maccabi_site_games

    @property
    def home_games(self):
        """
        :rtype: MaccabiSiteGamesWrapper
        """
        return MaccabiSiteGamesWrapper([game for game in self.games if game.maccabi_is_home_team])

    @property
    def away_games(self):
        """
        :rtype: MaccabiSiteGamesWrapper
        """
        return MaccabiSiteGamesWrapper([game for game in self.games if not game.maccabi_is_home_team])

    @property
    def available_competitions(self):
        return set(game.competition for game in self.games)

    def get_games_against_team(self, team_name):
        """
        :param team_name: str.
        :rtype: MaccabiSiteGamesWrapper
        """
        return MaccabiSiteGamesWrapper([game for game in self.games if team_name == game.not_maccabi_team.name])

    def played_before(self, date):
        return MaccabiSiteGamesWrapper([game for game in self.games if game.played_before(date)])

    def played_after(self, date):
        return MaccabiSiteGamesWrapper([game for game in self.games if game.played_after(date)])

    def get_games_by_competition(self, competition_type):
        """
        :type competition_type: CompetitionTypes or str
        :rtype: MaccabiSiteGamesWrapper
        """
        if type(competition_type) is str:
            return MaccabiSiteGamesWrapper([game for game in self.games if game.competition == competition_type])
        elif type(competition_type) is CompetitionTypes:
            return MaccabiSiteGamesWrapper([game for game in self.games if game.competition == competition_type.value])
        else:
            raise Exception("Enter string or CompetitionType")

    def __get_players_with_most_of_this_event(self, event_type):
        """
        :type event_type: GameEventTypes
        :rtype: Counter
        """
        players_with_most_event_type = reduce(
            lambda events_counter_a, events_counter_b: events_counter_a + events_counter_b,

            # TeamInGame saves dict which map between player event to the property
            # which return the most common players which have this event in this game & team.
            [game.maccabi_team.event_type_to_property_of_most_common_players[event_type]
             for game in self.games])

        # Remove the events by cast player_in_game to 'player' object
        return Counter(
            {player_in_game.get_as_normal_player(): players_with_most_event_type[player_in_game] for player_in_game
             in
             players_with_most_event_type}).most_common()

    @property
    def best_scorers(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.GOAL_SCORE)

    @property
    def best_assist(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.GOAL_ASSIST)

    @property
    def most_yellow_carded_players(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.YELLOW_CARD)

    @property
    def most_red_carded_players(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.RED_CARD)

    @property
    def most_substitute_off_players(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.SUBSTITUTION_OUT)

    @property
    def most_substitute_in_players(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.SUBSTITUTION_IN)

    @property
    def most_lineup_players(self):
        return self.__get_players_with_most_of_this_event(GameEventTypes.LINE_UP)

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

    def __len__(self):
        return len(self.games)

    def __getitem__(self, item):
        """
        :rtype: MaccabiSiteGameParser
        """
        return self.games[item]
