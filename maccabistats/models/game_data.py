# -*- coding: utf-8 -*-

import datetime
import json
from dateutil.parser import parse as datetime_parser
from maccabistats.models.player_game_events import GameEventTypes, GoalTypes


class GameData(object):
    def __init__(self, competition, fixture, date_as_hebrew_string, stadium, crowd, referee, home_team, away_team,
                 is_maccabi_home_team, season_string, half_parsed_events, date=None):
        """
        :param competition: cup, league and so on.
        :type competition: str
        :type fixture: str
        :type date_as_hebrew_string: str
        :type stadium: str
        :type crowd: str
        :type referee: str
        :type home_team: maccabistats.models.team_in_game.TeamInGame
        :type away_team: maccabistats.models.team_in_game.TeamInGame
        :type is_maccabi_home_team: bool
        :param season_string: season description, such as : 2000-2001 or 2000-01
        :type season_string: str
        :param half_parsed_events: events which had problem while parsing or validating, should be use for manipulating the game data later.
        :type half_parsed_events: list of dict
        :param date: the date the game was played.
        :type date: datetime.datetime
        """

        self.competition = competition
        self.fixture = fixture
        #todo get this shit out of here
        self.date_as_hebrew_string = date_as_hebrew_string
        self.date = self.__get_date_as_datetime() if date is None else date  # Leave only the year & month & day
        self.stadium = stadium
        self.crowd = crowd
        self.referee = referee
        self.home_team = home_team
        self.away_team = away_team
        self.is_maccabi_home_team = is_maccabi_home_team
        self.season = season_string
        self._half_parsed_events = half_parsed_events

    def played_before(self, date):
        """
        :type date: datetime.datetime or str
        :rtype: bool
        """

        if type(date) is str:
            date = datetime_parser(date)
        return date >= self.date

    def played_after(self, date):
        """
        :type date: datetime.datetime or str
        :rtype: bool
        """

        if type(date) is str:
            date = datetime_parser(date)
        return date <= self.date

    def __get_date_as_datetime(self):
        """
        :rtype: datetime.datetime
        """
        date_args = self.date_as_hebrew_string.strip().split(" ")
        return datetime.datetime(year=int(date_args[2]), month=GameData.__get_month_num_from_hebrew(date_args[1]),
                                 day=int(date_args[0]))

    @staticmethod
    def __get_month_num_from_hebrew(month_name):
        """
        :type month_name: str
        :rtype: int
        """
        months_in_hebrew_to_num = {"ינו": 1, "פבר": 2, "מרץ": 3, "אפר": 4, "מאי": 5, "יונ": 6, "יול": 7, "אוג": 8,
                                   "ספט": 9, "אוק": 10,
                                   "נוב": 11, "דצמ": 12}

        return months_in_hebrew_to_num[month_name]

    @property
    def maccabi_score(self):
        return self.maccabi_team.score

    @property
    def maccabi_score_diff(self):
        return self.maccabi_team.score - self.not_maccabi_team.score

    @property
    def maccabi_team(self):
        """ :rtype: maccabistats.models.team_in_game.TeamInGame """

        if self.is_maccabi_home_team:
            return self.home_team
        else:
            return self.away_team

    @property
    def not_maccabi_team(self):
        """ :rtype: maccabistats.models.team_in_game.TeamInGame """

        if self.is_maccabi_home_team:
            return self.away_team
        else:
            return self.home_team

    @property
    def is_maccabi_win(self):
        """ :rtype: bool """
        return self.maccabi_score_diff > 0

    @property
    def events(self):
        """
        Return all players events from maccabi_team in this game.
        :return: Each list entry contains:
                    normal_players dict, event.to_json, team_name.
                List is ordered by event_time asc.
        :rtype: list of dict
        """

        # Maccabi team players events
        players_events = [dict(player.get_as_normal_player().__dict__,  # Players attributes, normal -> no events.
                               **event.json_dict(),
                               team=self.maccabi_team.name)
                          for player in self.maccabi_team.players
                          for event in player.events]

        # Not maccabi team players events
        players_events.extend([dict(player.get_as_normal_player().__dict__,  # Players attributes, normal -> no events.
                                    **event.json_dict(),
                                    team=self.not_maccabi_team.name)
                               for player in self.not_maccabi_team.players
                               for event in player.events])

        sorted_players_events = sorted(players_events, key=lambda p: p['time_occur'])  # Sort by event time.

        return sorted_players_events

    def goals(self):
        """
        Return list of game events which their type is goal (ordered by time).
        Each event contains the results of the game as it was AFTER the goal was scored.
        :return: list of maccabistats.models.player_game_events.GameEvent
        """

        goals_events = [event for event in self.events if event['event_type'] == GameEventTypes.GOAL_SCORE.value]
        maccabi_score = not_maccabi_score = 0

        for goal in goals_events:
            if goal['team'] == "מכבי תל אביב":
                if goal['goal_type'] == GoalTypes.OWN_GOAL.value:
                    not_maccabi_score += 1
                else:
                    maccabi_score += 1
            else:
                if goal['goal_type'] == GoalTypes.OWN_GOAL.value:
                    not_maccabi_score += 1
                else:
                    maccabi_score += 1

            goal['maccabi_score'] = maccabi_score
            goal['not_maccabi_score'] = not_maccabi_score

        return goals_events

    def json_dict(self):
        """
        :rtype: dict
        """
        return dict(stadium=self.stadium,
                    date=self.date.isoformat(),
                    crowd=self.crowd,
                    referee=self.referee,
                    competition=self.competition,
                    fixture=self.fixture,
                    home_team=self.home_team.json_dict(),
                    away_team=self.away_team.json_dict())

    def to_json(self):
        return json.dumps(self.json_dict())

    def __repr__(self):
        return "Game between {self.home_team.name} (home) - {self.away_team.name} (away)\n" \
               "Results : {self.home_team.score} - {self.away_team.score}\n" \
               "Played on {self.stadium} at {self.date} with {self.crowd} viewers\n" \
               "As part of {self.competition}, round - {self.fixture}\n" \
               "Referee : {self.referee}\n" \
               "HomeTeam : {self.home_team}\n" \
               "AwayTeam : {self.away_team}\n\n".format(self=self)
