def test__export_to_json__no_errors_should_be_thrown(tmp_path, maccabipedia_maccabistats):
    maccabipedia_maccabistats.export.to_flatten_json(tmp_path / 'temp.json')


def test__export_to_csv__no_errors_should_be_thrown(tmp_path, maccabipedia_maccabistats):
    maccabipedia_maccabistats.export.to_flatten_csv(tmp_path / 'temp.csv')
