# -*- coding: utf-8 -*-


from maccabistats.config.config import get_str_from_settings

# This file contains all the settings.ini file related

section_name_in_settings = "maccabipedia"

base_crawling_address = "base-crawling-address"
games_table_name = "games-query-tables-names"
games_table_fields = "games-query-tables-fields"
games_query_join_on = "games-query-join-on"
games_events_table_name = "games-events-query-tables-names"
games_events_table_fields = "games-events-query-tables-fields"


def get_base_crawling_address_from_settings():
    return get_str_from_settings(section_name_in_settings, base_crawling_address)


def get_games_table_name_from_settings():
    return get_str_from_settings(section_name_in_settings, games_table_name)


def get_games_table_fields_from_settings():
    return get_str_from_settings(section_name_in_settings, games_table_fields)


def get_games_query_join_on_from_settings():
    return get_str_from_settings(section_name_in_settings, games_query_join_on)


def get_games_events_table_name_from_settings():
    return get_str_from_settings(section_name_in_settings, games_events_table_name)


def get_games_events_table_fields_from_settings():
    return get_str_from_settings(section_name_in_settings, games_events_table_fields)
