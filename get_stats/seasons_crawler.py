#!/usr/bin/python
# -*- coding: utf-8 -*-

from get_stats.seasons_from_maccabi_site import get_parsed_maccabi_site_seasons

if __name__ == '__main__':
    # save_all_maccabi_game_web_pages_to_disk()
    wow = get_parsed_maccabi_site_seasons()

    """
    import pickle
    with open(r"F:\maccabi-code\projects\all-data.pickle", 'wb') as f:
        pickle.dump(wow, f)
    """
