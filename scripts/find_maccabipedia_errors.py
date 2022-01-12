import logging

from maccabistats import run_maccabipedia_source, ErrorsFinder

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    logging.info('Starting to find errors from MaccabiPedia')

    maccabipedia_games = run_maccabipedia_source()
    logging.info(f'MaccabiPedia games: {maccabipedia_games}')

    errors_finder = ErrorsFinder(maccabipedia_games)
    errors_finder.get_all_errors_numbers()

    logging.info('Finished to find errors from MaccabiPedia')
