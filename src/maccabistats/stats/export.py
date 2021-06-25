from __future__ import annotations

import csv
import itertools
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Any, List, Optional

from maccabistats.models.game_data import GameData

if TYPE_CHECKING:
    from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats

logger = logging.getLogger(__name__)

FlattenGame = List[Dict[str, Any]]

_BASE_EXPORT_FOLDER = Path.home() / 'maccabistats' / 'export'

_OPTIONAL_EVENT_PROPERTIES = ['player_goal_type']


class ExportMaccabiGamesStats(object):
    """
    This class will serialize MaccabiGamesStats into readable/useful formats, like json, csv and so on.
    """

    def __init__(self, maccabi_games_stats: MaccabiGamesStats):
        self.maccabi_games_stats = maccabi_games_stats

    @staticmethod
    def _flatten_dict_game(game: GameData) -> FlattenGame:
        game_data = dict(stadium=game.stadium,
                         date=game.date.isoformat(),
                         crowd=game.crowd,
                         referee=game.referee,
                         competition=game.competition,
                         fixture=game.fixture,
                         season=game.season,
                         technical_result=game.technical_result,
                         home_team_name=game.home_team.name,
                         home_team_score=game.home_team.score,
                         home_team_coach=game.home_team.coach,
                         away_team_name=game.away_team.name,
                         away_team_score=game.away_team.score,
                         away_team_coach=game.away_team.coach)

        game_events = []

        for current_event_data in game.events:
            # In order to prevent name collision and make te data more readable:
            event_data_with_player_prefix = {f'player_{key}': value for key, value in current_event_data.items()}

            game_events.append({**game_data, **event_data_with_player_prefix})

        return game_events

    def _flatten_dict_all_games(self) -> List[FlattenGame]:
        all_games = []

        for game in self.maccabi_games_stats:
            current_game_data = self._flatten_dict_game(game)

            if not current_game_data:
                logger.warning(f'Game: {game} is empty, could not serialize it, skipping it')
                continue

            all_games.append(current_game_data)

        return all_games
v
    def to_flatten_json(self, file_path: Optional[Path] = None) -> None:
        file_path = file_path or _BASE_EXPORT_FOLDER / 'flatten_maccabistats.json'
        file_path.parent.mkdir(parents=True, exist_ok=True)

        games_data = itertools.chain.from_iterable(self._flatten_dict_all_games())

        jsoned_data = json.dumps(list(games_data), indent=4, ensure_ascii=False)
        file_path.write_text(jsoned_data, encoding='utf8')

        logger.info(f'Wrote the MaccabiGamesStats data to: {file_path} successfully!')

    def to_flatten_csv(self, file_path: Optional[Path] = None) -> None:
        file_path = file_path or _BASE_EXPORT_FOLDER / 'flatten_maccabistats.csv'
        file_path.parent.mkdir(parents=True, exist_ok=True)

        games_data = itertools.chain.from_iterable(self._flatten_dict_all_games())
        first_game = next(games_data)

        with file_path.open(mode='w', encoding='utf8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    delimiter=',',
                                    fieldnames=list(first_game.keys()) + _OPTIONAL_EVENT_PROPERTIES)
            writer.writeheader()

            writer.writerow(first_game)  # Because we popped it out to set the header
            writer.writerows(games_data)

        logger.info(f'Wrote the MaccabiGamesStats data to: {file_path} successfully!')
