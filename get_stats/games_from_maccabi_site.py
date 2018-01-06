#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup

folder_to_save_games_html_files = r"F:\maccabi-code\games"
folder_to_save_games_events_html_files_pattern = os.path.join(folder_to_save_games_html_files, "game+{game_date}+events")
folder_to_save_games_squads_html_files_pattern = os.path.join(folder_to_save_games_html_files, "game+{game_date}+squads")


def save_game_web_page_to_disk(web_page):
    """
    :type web_page: str
    """

    game_events_web_page_content = requests.get(web_page).content
    game_squads_web_page_content = requests.get(web_page + "teams").content

    game_date = __extract_games_date(web_page)
    with open(folder_to_save_games_events_html_files_pattern.format(game_date=game_date), 'wb') as maccabi_game_event_file:
        maccabi_game_event_file.write(game_events_web_page_content)
    with open(folder_to_save_games_squads_html_files_pattern.format(game_date=game_date), 'wb') as maccabi_game_squad_file:
        maccabi_game_squad_file.write(game_squads_web_page_content)


def __extract_games_date(link):
    web_page = link.strip("/")  # Remove / at the end if exists for rsplit.
    game_date = web_page.rsplit("/")[-1]
    return game_date


def get_game_events_bs_by_link(link):
    game_date = __extract_games_date(link)
    with open(folder_to_save_games_events_html_files_pattern.format(game_date=game_date), 'rb') as game_events_file:
        return BeautifulSoup(game_events_file.read(), "html.parser")


def get_game_squads_bs_by_link(link):
    game_date = __extract_games_date(link)
    with open(folder_to_save_games_squads_html_files_pattern.format(game_date=game_date), 'rb') as game_squads_file:
        return BeautifulSoup(game_squads_file.read(), "html.parser")
