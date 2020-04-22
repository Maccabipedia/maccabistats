from collections import defaultdict

from dateutil.parser import parse as datetime_parser

from maccabistats.parse.maccabipedia.maccabipedia_cargo_chunks_crawler import MaccabiPediaCargoChunksCrawler


class MaccabiPediaPlayers(object):
    missing_birth_date_value = datetime_parser("1000")
    _instance = None

    @classmethod
    def default_birth_day_value(cls, *args, **kwargs):
        return cls.missing_birth_date_value

    def __init__(self):
        # Uses defaultdict, each player that does not have a date of birth in maccabipedia, will set to year 1000 (to notice visually in stats)
        self.players_dates = defaultdict(MaccabiPediaPlayers.default_birth_day_value, self.crawl_players_birth_dates())

    @staticmethod
    def crawl_players_birth_dates():
        """
        :rtype: dict[str, datetime.datetime]
        """
        players_date_of_birth_iterator = MaccabiPediaCargoChunksCrawler(tables_name="Profiles", tables_fields="Profiles._pageName, Profiles.DoB")
        players_birth_dates = dict()
        for player_data in players_date_of_birth_iterator:
            if not player_data['DoB']:
                continue  # We use defaultdict, These players will count as born at year 1000

            player_name = player_data['_pageName']
            players_birth_dates[player_name] = datetime_parser(player_data['DoB'])

        return players_birth_dates

    @classmethod
    def get_players_data(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
