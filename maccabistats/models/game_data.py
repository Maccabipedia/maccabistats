# -*- coding: utf-8 -*-

import datetime


class GameData(object):
    def __init__(self, competition, fixture, date_as_hebrew_string, stadium, crowd, referee, home_team, away_team, is_maccabi_home_team):
        """
        :param competition: cup, league and so on.
        :type competition: str.
        :type fixture: str.
        :type date_as_hebrew_string: str.
        :type stadium: str.
        :type crowd: str.
        :type referee: str.
        :type home_team: maccabistats.models.team_in_game.TeamInGame
        :type away_team: maccabistats.models.team_in_game.TeamInGame
        :type is_maccabi_home_team: bool.
        """

        self.competition = competition
        self.fixture = fixture
        self.date_as_hebrew_string = date_as_hebrew_string
        self.date = self.__get_date_as_datetime()
        self.stadium = stadium
        self.crowd = crowd
        self.referee = referee
        self.home_team = home_team
        self.away_team = away_team
        self.is_maccabi_home_team = is_maccabi_home_team

    def played_before(self, date):
        """
        :type date: datetime.datetime or str
        :rtype: bool
        """

        if type(date) is str:
            date_args = date.strip().split(".")
            date = datetime.datetime(year=int(date_args[2]), month=int(date_args[1]), day=int(date_args[0]))
        return date >= self.date

    def played_after(self, date):
        """
        :type date: datetime.datetime or str
        :rtype: bool
        """

        if type(date) is str:
            date_args = date.strip().split(".")
            date = datetime.datetime(year=int(date_args[2]), month=int(date_args[1]), day=int(date_args[0]))
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
        """ :rtype: TeamInGame """

        if self.is_maccabi_home_team:
            return self.home_team
        else:
            return self.away_team

    @property
    def not_maccabi_team(self):
        """ :rtype: TeamInGame """

        if self.is_maccabi_home_team:
            return self.away_team
        else:
            return self.home_team

    @property
    def is_maccabi_win(self):
        """ :rtype: bool """
        return self.maccabi_score_diff > 0

    def __repr__(self):
        return "Game between {self.home_team.name} (home) - {self.away_team.name} (away)\n" \
               "Results : {self.home_team.score} - {self.away_team.score}\n" \
               "Played on {self.stadium} at {self.date} with {self.crowd} viewers\n" \
               "As part of {self.competition}, round - {self.fixture}\n" \
               "Referee : {self.referee}\n" \
               "HomeTeam : {self.home_team}\n" \
               "AwayTeam : {self.away_team}\n\n".format(self=self)
