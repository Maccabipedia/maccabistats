from __future__ import annotations

import datetime
import json
import logging
from collections import defaultdict
from tempfile import NamedTemporaryFile
from typing import List, Union, Dict, Any

from dateutil.parser import parse as datetime_parser

from maccabistats.models.game_data import GameData
from maccabistats.models.player import Player
from maccabistats.stats.averages import MaccabiGamesAverageStats
from maccabistats.stats.coaches import MaccabiGamesCoachesStats
from maccabistats.stats.comebacks import MaccabiGamesComebacksStats
from maccabistats.stats.consts import TROPHY_COMPETITIONS, EUROPE_COMPETITIONS, LEAGUE_COMPETITIONS, \
    NON_OFFICIAL_COMPETITIONS
from maccabistats.stats.graphs import MaccabiGamesGraphsStats
from maccabistats.stats.important_goals import MaccabiGamesImportantGoalsStats
from maccabistats.stats.players import MaccabiGamesPlayersStats
from maccabistats.stats.players_categories import MaccabiGamesPlayersCategoriesStats
from maccabistats.stats.players_events_sumamry import MaccabiGamesPlayersEventsSummaryStats
from maccabistats.stats.players_first_and_last_games import MaccabiGamesPlayersFirstAndLastGamesStats
from maccabistats.stats.players_special_games import MaccabiGamesPlayersSpecialGamesStats
from maccabistats.stats.players_streaks import MaccabiGamesPlayersStreaksStats
from maccabistats.stats.referees import MaccabiGamesRefereesStats
from maccabistats.stats.results import MaccabiGamesResultsStats
from maccabistats.stats.seasons import MaccabiGamesSeasonsStats
from maccabistats.stats.streaks import MaccabiGamesStreaksStats
from maccabistats.stats.teams import MaccabiGamesTeamsStats
from maccabistats.stats.teams_streaks import MaccabiGamesTeamsStreaksStats
from maccabistats.version import version as maccabistats_version

logger = logging.getLogger(__name__)


class MaccabiGamesStats(object):

    def __init__(self, maccabi_games: List[GameData]) -> None:
        self.games: List[GameData] = sorted(maccabi_games, key=lambda g: g.date)  # Sort the games by date

        self.coaches = MaccabiGamesCoachesStats(self)
        self.players = MaccabiGamesPlayersStats(self)
        self.streaks = MaccabiGamesStreaksStats(self)
        self.averages = MaccabiGamesAverageStats(self)
        self.results = MaccabiGamesResultsStats(self)
        self.referees = MaccabiGamesRefereesStats(self)
        self.comebacks = MaccabiGamesComebacksStats(self)
        self.seasons = MaccabiGamesSeasonsStats(self)
        self.important_goals = MaccabiGamesImportantGoalsStats(self)
        self.graphs = MaccabiGamesGraphsStats(self)
        self.players_streaks = MaccabiGamesPlayersStreaksStats(self)
        self.teams_streaks = MaccabiGamesTeamsStreaksStats(self)
        self.teams = MaccabiGamesTeamsStats(self)
        self.players_events_summary = MaccabiGamesPlayersEventsSummaryStats(self)
        self.players_special_games = MaccabiGamesPlayersSpecialGamesStats(self)
        self.players_first_and_last_games = MaccabiGamesPlayersFirstAndLastGamesStats(self)
        self.players_categories = MaccabiGamesPlayersCategoriesStats(self)

        self.version = maccabistats_version

    # region home_away

    @property
    def home_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.is_maccabi_home_team])

    @property
    def away_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if not game.is_maccabi_home_team])

    # endregion

    # region competitions filters

    @property
    def trophy_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.competition in TROPHY_COMPETITIONS])

    @property
    def europe_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.competition in EUROPE_COMPETITIONS])

    @property
    def league_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.competition in LEAGUE_COMPETITIONS])

    @property
    def official_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.competition not in NON_OFFICIAL_COMPETITIONS])

    @property
    def non_official_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.competition in NON_OFFICIAL_COMPETITIONS])

    # endregion

    # region available properties

    @property
    def available_competitions(self) -> List[str]:
        return list(set(game.competition for game in self.games))

    @property
    def available_opponents(self) -> List[str]:
        return list(set(game.not_maccabi_team.name for game in self.games))

    @property
    def available_stadiums(self) -> List[str]:
        return list(set(game.stadium for game in self.games))

    @property
    def available_players(self) -> List[Player]:
        """
        Returns players objects (name + number), Which means a player name can appear more than once.
        """
        players = set(player for game in self.games for player in game.maccabi_team.players)
        return list(set([player.get_as_normal_player() for player in players]))

    @property
    def available_players_names(self) -> List[str]:
        return list(set(player.name for player in self.available_players))

    @property
    def available_referees(self) -> List[str]:
        return list(set(game.referee for game in self.games))

    @property
    def available_coaches(self) -> List[str]:
        return list(set(game.maccabi_team.coach for game in self.games))

    @property
    def available_seasons(self) -> List[str]:
        return sorted(list(set(game.season for game in self.games)))

    # endregion

    # region result based

    @property
    def maccabi_wins(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.is_maccabi_win])

    @property
    def maccabi_ties(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.maccabi_score_diff == 0])

    @property
    def maccabi_losses(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.maccabi_score_diff < 0])

    @property
    def technical_result_games(self) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.technical_result])

    # endregion

    # region date based

    def played_before(self, date: Union[datetime.datetime, datetime.date, str]) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.played_before(date)])

    def played_after(self, date: Union[datetime.datetime, datetime.date, str]) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if game.played_after(date)])

    def played_at(self, date: Union[datetime.datetime, datetime.date, str]) -> MaccabiGamesStats:
        if isinstance(date, str):
            date = datetime_parser(date).date()
        elif isinstance(date, datetime.datetime):
            date = date.date()  # Leave only year & month & day

        return MaccabiGamesStats([game for game in self.games if game.date.date() == date])

    @property
    def first_game_date(self) -> str:
        return self[0].date.strftime('%d-%m-%Y')

    @property
    def last_game_date(self) -> str:
        return self[-1].date.strftime('%d-%m-%Y')

    # endregion

    # region free-style filters

    def get_games_by_competition(self, competition_types: Union[List[str], str]) -> MaccabiGamesStats:
        if isinstance(competition_types, str):
            competition_types = [competition_types]

        return MaccabiGamesStats([game for game in self.games if game.competition in competition_types])

    def get_games_by_stadium(self, stadium_name: str) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if stadium_name == game.stadium])

    def get_games_against_team(self, team_name: str) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if team_name == game.not_maccabi_team.name])

    def get_games_by_coach(self, coach_name: str) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if coach_name == game.maccabi_team.coach])

    def get_games_by_referee(self, referee_name: str) -> MaccabiGamesStats:
        return MaccabiGamesStats([game for game in self.games if referee_name == game.referee])

    def get_games_with_player_name(self, player_name: str) -> MaccabiGamesStats:
        """
        Returns all the games that this player have any event in, played or at the bench.
        """
        return MaccabiGamesStats([game for game in self.games
                                  if player_name in [p.name.strip() for p in game.maccabi_team.players]])

    def get_games_by_played_player_name(self, player_name: str) -> MaccabiGamesStats:
        """
        Returns all the games that the given players played at.
        """
        return MaccabiGamesStats([game for game in self.games
                                  if player_name in [p.name.strip() for p in game.maccabi_team.played_players]])

    def get_games_by_season(self, season: str) -> MaccabiGamesStats:
        """
        Return Maccabi games stats object with season games, season may be entered as "1900/01".
        """
        return MaccabiGamesStats([game for game in self.games if game.season == season])

    # endregion

    def games_by_player_name(self) -> Dict[str, MaccabiGamesStats]:
        """
        Returns a mapping between a player name to all of his games
        """
        players_games = defaultdict(list)

        for game in self.games:
            for player in game.maccabi_team.players:
                players_games[player.name].append(game)

        return {player_name: MaccabiGamesStats(players_games[player_name]) for player_name in players_games.keys()}

    @classmethod
    def create_maccabi_stats_from_games(cls, games: List[GameData]) -> MaccabiGamesStats:
        return cls(games)

    def get_summary(self) -> Dict[str, Any]:
        summary = {'games': len(self),
                   "wins": self.results.wins_count,
                   "wins_by_percentage": self.results.wins_percentage,
                   "losses": self.results.losses_count,
                   "losses_by_percentage": self.results.losses_percentage,
                   "ties": self.results.ties_count,
                   "ties_by_percentage": self.results.ties_percentage,
                   "goals_for_maccabi": self.results.total_goals_for_maccabi,
                   "goals_for_maccabi_avg": self.averages.goals_for_maccabi,
                   "goals_against_maccabi": self.results.total_goals_against_maccabi,
                   "goals_against_maccabi_avg": self.averages.goals_against_maccabi,
                   "goals_diff_for_maccabi": self.results.total_goals_diff_for_maccabi,
                   "goals_diff_for_maccabi_avg": self.averages.maccabi_diff}

        return summary

    def show_summary(self) -> None:
        summary = ("Maccabi games stats object:"
                   "\n\nGames count: {games}"
                   "\nWins : {wins} ({wins_by_percentage}%)"
                   "\nLosses : {losses} ({losses_by_percentage}%)"
                   "\nTies : {ties} ({ties_by_percentage}%)"
                   "\n\nGoals for maccabi : {goals_for_maccabi}, {goals_for_maccabi_avg} per game"
                   "\nGoals against maccabi : {goals_against_maccabi}, {goals_against_maccabi_avg} per game"
                   "\nGoals diff for maccabi: {goals_diff_for_maccabi}, {goals_diff_for_maccabi} per game").format(
            **self.get_summary())

        print(summary)

    def to_json(self) -> str:
        return json.dumps([game.to_json() for game in self.games], indent=4)

    def serialize_to_json(self) -> None:
        # TODO, there is too much escaped stuff in this function output
        with NamedTemporaryFile(delete=False, mode='w') as temp_json:
            logger.info(f"Serializing current maccabi games stats to temporary json file at: {temp_json.name}")
            temp_json.file.write(self.to_json())

    def __len__(self) -> int:
        return len(self.games)

    def __getitem__(self, item) -> GameData:
        return self.games[item]

    def __iter__(self):
        for game in self.games:
            yield game

    def __repr__(self) -> str:
        summary = f"{len(self)} games"
        if len(self) > 0:
            summary += f" (from {self.first_game_date} to {self.last_game_date})"

        return summary

    @property
    def hebrew_representation(self) -> str:
        summary = f"{len(self)} משחקים"
        if len(self) > 0:
            summary += f" (החל מ {self.first_game_date} ועד {self.last_game_date})"

        return summary
