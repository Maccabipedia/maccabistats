# -*- coding: utf-8 -*-

from maccabistats.parse.maccabi_tlv_site.config import get_folder_to_save_games_html_files_from_settings, \
    get_should_use_disk_to_crawl_when_available_from_settings

import os
import requests
from bs4 import BeautifulSoup

folder_to_save_games_events_html_files_pattern = os.path.join(get_folder_to_save_games_html_files_from_settings(),
                                                              "game+{game_date}+events")
folder_to_save_games_squads_html_files_pattern = os.path.join(get_folder_to_save_games_html_files_from_settings(),
                                                              "game+{game_date}+squads")


def save_game_web_page_to_disk(web_page):
    """
    :type web_page: str
    """

    game_events_web_page_content = requests.get(web_page).content
    game_squads_web_page_content = requests.get(web_page + "teams").content

    game_date = __extract_games_date(web_page)
    with open(folder_to_save_games_events_html_files_pattern.format(game_date=game_date),
              'wb') as maccabi_game_event_file:
        maccabi_game_event_file.write(game_events_web_page_content)
    with open(folder_to_save_games_squads_html_files_pattern.format(game_date=game_date),
              'wb') as maccabi_game_squad_file:
        maccabi_game_squad_file.write(game_squads_web_page_content)


def __extract_games_date(link):
    web_page = link.strip("/")  # Remove / at the end if exists for rsplit.
    game_date = web_page.rsplit("/")[-1]
    return game_date


# GameEvents #

def __get_game_events_bs_from_disk(link):
    game_date = __extract_games_date(link)

    with open(folder_to_save_games_events_html_files_pattern.format(game_date=game_date), 'rb') as game_events_file:
        return BeautifulSoup(game_events_file.read(), "html.parser")


def __does_game_events_bs_exists_on_disk(link):
    game_date = __extract_games_date(link)

    return os.path.isfile(folder_to_save_games_events_html_files_pattern.format(game_date=game_date))


def __get_game_events_bs_from_internet(link):
    return requests.get(link).content


def __download_game_events_page(link):
    game_events_web_page_content = __get_game_events_bs_from_internet(link)
    __save_game_events_bs_to_disk(link, game_events_web_page_content)
    return __get_game_events_bs_from_disk(link)


def __save_game_events_bs_to_disk(link, content):
    game_date = __extract_games_date(link)

    with open(folder_to_save_games_events_html_files_pattern.format(game_date=game_date),
              'wb') as maccabi_game_event_file:
        maccabi_game_event_file.write(content)


def get_game_events_bs_by_link(link):
    if get_should_use_disk_to_crawl_when_available_from_settings():
        if __does_game_events_bs_exists_on_disk(link):
            return __get_game_events_bs_from_disk(link)
        else:
            return __download_game_events_page(link)
    else:
        return __download_game_events_page(link)


# GameSquads #

def __get_game_squads_bs_from_disk(link):
    game_date = __extract_games_date(link)

    with open(folder_to_save_games_squads_html_files_pattern.format(game_date=game_date), 'rb') as game_squads_file:
        return BeautifulSoup(game_squads_file.read(), "html.parser")


def __does_game_squads_bs_exists_on_disk(link):
    game_date = __extract_games_date(link)

    return os.path.isfile(folder_to_save_games_squads_html_files_pattern.format(game_date=game_date))


def __get_game_squads_bs_from_internet(link):
    return requests.get(link + "teams").content


def __download_game_squads_page(link):
    game_squads_web_page_content = __get_game_squads_bs_from_internet(link)
    __save_game_squads_bs_to_disk(link, game_squads_web_page_content)
    return __get_game_squads_bs_from_disk(link)


def __save_game_squads_bs_to_disk(link, content):
    game_date = __extract_games_date(link)

    with open(folder_to_save_games_squads_html_files_pattern.format(game_date=game_date),
              'wb') as maccabi_game_squad_file:
        maccabi_game_squad_file.write(content)


def get_game_squads_bs_by_link(link):
    if get_should_use_disk_to_crawl_when_available_from_settings():
        if __does_game_squads_bs_exists_on_disk(link):
            return __get_game_squads_bs_from_disk(link)
        else:
            return __download_game_squads_page(link)
    else:
        return __download_game_squads_page(link)
