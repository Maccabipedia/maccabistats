# -*- coding: utf-8 -*-


import os
import configparser


settings_file_folder_path = os.path.dirname(os.path.abspath(__file__))
settings_file_path = os.path.join(settings_file_folder_path, "settings.ini")


def __get_config_parser_object():
    """
    :rtype :configparser.ConfigParser
    """
    c = configparser.ConfigParser()
    c.read(settings_file_path, encoding='utf-8-sig')
    return c


def get_int_from_settings(section_name, key_name):
    """ Return [key_name] from [section_name] section in settings.ini
    :rtype : int.
    """
    return __get_config_parser_object().getint(section_name, key_name)


def get_str_from_settings(section_name, key_name):
    """ Return [key_name] from [section_name] section in settings.ini
    :rtype : str.
    """
    return __get_config_parser_object().get(section_name, key_name)


def get_bool_from_settings(section_name, key_name):
    """ Return [key_name] from [section_name] section in settings.ini
    :rtype : str.
    """
    return __get_config_parser_object().getboolean(section_name, key_name)

