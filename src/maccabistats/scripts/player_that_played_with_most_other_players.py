from pprint import pformat

from maccabistats import *

if __name__ == '__main__':
    maccabipedia_games = load_from_maccabipedia_source().official_games

    # Change 'games_by_player_name' players games to be just "played players" from maccabi and not in the squad
    players_games = maccabipedia_games.played_games_by_player_name()
    players_to_available_players_len = dict()

    for player_name, games in players_games.items():
        # Get just the played players, -1 himself
        players_to_available_players_len[player_name] = len(games.players.most_played) - 1

    most_played_with_others_player = sorted(players_to_available_players_len.items(), key=lambda item: item[1],
                                            reverse=True)
    print(f'Top: {pformat(most_played_with_others_player[:20])}')
