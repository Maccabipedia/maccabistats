import json
import logging
from pathlib import Path

import requests

from maccabistats.stats.maccabi_games_stats import MaccabiGamesStats
from .common import get_player_id_by_player_name, FAKE_USER_AGENT, PLAYER_STATS_URL_PATTERN_UNFORMATTED

_logger = logging.getLogger(__name__)

_better_names = {'מיקו בלו': 'מנחם בלו'}


class TransfermarktFetcher:
    def __init__(self, maccabi_games_stats: MaccabiGamesStats, data_storage_folder: Path):
        self.maccabi_games_stats = maccabi_games_stats
        self.data_storage_folder = data_storage_folder

        if self.players_ids_file.is_file():
            self.players_ids = json.loads(self.players_ids_file.read_text(encoding='utf8'))
        else:
            self.players_ids = {}

    @property
    def players_ids_file(self) -> Path:
        return self.data_storage_folder / 'players_id.json'

    def _dump_player_id_to_file(self) -> None:
        self.players_ids_file.write_text(data=json.dumps(self.players_ids), encoding='utf8')

    def fetch(self, force_refetch: bool = False) -> None:
        _logger.info(f'Fetching data to {self.data_storage_folder}, force_refetch: {force_refetch}')
        self.data_storage_folder.mkdir(parents=True, exist_ok=True)

        _logger.info(f'Fetching player by player, starting from these with the most appearances')

        for player_name, _ in self.maccabi_games_stats.players.most_played:
            player_name = _better_names.get(player_name, player_name)

            # noinspection PyBroadException
            try:
                self._fetch_one_player(player_name, force_refetch)
                _logger.info(f'Fetched {player_name} successfully!')
            except Exception:
                _logger.exception(f'Could not fetch player: {player_name} data, due to: ')

    def _fetch_one_player(self, player_name: str, force_refetch: bool) -> None:
        player_html_file = self.data_storage_folder / f'{player_name}.html'

        if not force_refetch and player_html_file.exists():
            _logger.info(f'player: {player_name} html already exists: {player_html_file}, skipping it')
            return

        _logger.info(f'Fetching player: {player_name} to: {player_html_file}')
        player_id = self.players_ids.get(player_name, get_player_id_by_player_name(player_name))

        player_url_response = requests.get(url=PLAYER_STATS_URL_PATTERN_UNFORMATTED.format(player_id=player_id),
                                           headers=FAKE_USER_AGENT)
        player_url_response.raise_for_status()

        player_html_file.write_bytes(player_url_response.content)

        # In case everything work, let's cache it
        self.players_ids[player_name] = player_id
        self._dump_player_id_to_file()
