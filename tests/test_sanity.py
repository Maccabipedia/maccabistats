def test_a(maccabipedia_maccabistats):
    # Just make sure we can iterate every game and access maccabi team object
    for game in maccabipedia_maccabistats:
        for maccabi_player in game.maccabi_team.players:
            assert maccabi_player.name
