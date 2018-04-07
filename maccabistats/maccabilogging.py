import logging
import os
from multiprocessing import current_process
from pathlib import Path
from enum import Enum
from glob import glob
from dateutil.parser import parse as parse_datetime
from maccabistats.parse.maccabi_tlv_site.config import get_use_multi_process_crawl_from_settings

log_root_folder_path = Path.home().as_posix()
log_file_path_pattern = os.path.join(log_root_folder_path, "maccabistats-logs", "{pname}", "maccabistats-{suffix}.log")
log_file_folder_path = os.path.dirname(log_file_path_pattern)
logs_format = '%(asctime)s::%(processName)s(%(process)d) %(name)s %(levelname)s --- %(funcName)s(l.%(lineno)d) :: %(message)s'
logs_separator = "||.||" if get_use_multi_process_crawl_from_settings() else ""  # PATCH

logger = logging.getLogger("maccabistats")


class LogFilesTypes(Enum):
    ALL_LEVELS = "all_logs"
    INFO = "info"
    WARNING = "warning"
    EXCEPTION = "exception"


class SpecificLevelFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno == self.__level


class MultiProcessSuffixFormatter(logging.Formatter):

    def format(self, record):
        return "{result}{suffix}".format(result=super(MultiProcessSuffixFormatter, self).format(record), suffix=logs_separator)


def faster_logging():
    # Patch, TODO - fix me later - remove just Not FileHandlers
    logger.info("Use faster logging, removing debug & stdout handlers")
    logger.removeHandler(logger.handlers[3])  # Without stdout
    logger.removeHandler(logger.handlers[0])  # Without Debug


def get_logs_root_folder():
    return os.path.dirname(get_logs_folder_for_this_process())


def get_logs_folder_for_this_process():
    return os.path.dirname(log_file_path_pattern.format(suffix=LogFilesTypes.ALL_LEVELS.value, pname=current_process().name))


def validate_logs_folder_exists():
    os.makedirs(get_logs_folder_for_this_process(), exist_ok=True)


def initialize_logging():
    # Root logger, so all other logger will inherit those handlers.

    # IMPORTANT- each change here may require change in "refresh_file_handler_paths_according_to_process_name"&"merge_logs_files_from_all_processes".

    validate_logs_folder_exists()
    process_name = current_process().name

    logger.setLevel(logging.DEBUG)

    # "::" used for splitting the string later
    # logs separator not needed on stdout
    advanced_formatter = MultiProcessSuffixFormatter(logs_format)
    stdout_formatter = logging.Formatter(logs_format)

    all_levels_handler = logging.FileHandler(
        log_file_path_pattern.format(suffix=LogFilesTypes.ALL_LEVELS.value, pname=process_name), 'w', encoding="utf-8")
    all_levels_handler.setFormatter(advanced_formatter)
    all_levels_handler.setLevel(logging.DEBUG)

    info_handler = logging.FileHandler(
        log_file_path_pattern.format(suffix=LogFilesTypes.INFO.value, pname=process_name), 'w', encoding="utf-8")
    info_handler.setFormatter(advanced_formatter)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(SpecificLevelFilter(logging.INFO))

    warning_handler = logging.FileHandler(
        log_file_path_pattern.format(suffix=LogFilesTypes.WARNING.value, pname=process_name), 'w', encoding="utf-8")
    warning_handler.setFormatter(advanced_formatter)
    warning_handler.setLevel(logging.WARNING)
    warning_handler.addFilter(SpecificLevelFilter(logging.WARNING))

    exception_handler = logging.FileHandler(
        log_file_path_pattern.format(suffix=LogFilesTypes.EXCEPTION.value, pname=process_name), 'w', encoding="utf-8")
    exception_handler.setFormatter(advanced_formatter)
    exception_handler.setLevel(logging.ERROR)
    exception_handler.addFilter(SpecificLevelFilter(logging.ERROR))

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(stdout_formatter)
    stdout_handler.setLevel(logging.INFO)

    logger.addHandler(all_levels_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(stdout_handler)
    logger.addHandler(exception_handler)

    logger.debug("Initialize logger")


def initialize_logging_for_this_process():
    """
    This function use to change all file paths of file handlers, because multiprocess logging on windows is shit, so we use file per process.
    """

    validate_logs_folder_exists()

    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            # Patch
            handler.baseFilename = handler.baseFilename.replace("MainProcess", current_process().name)


# THIS IS NOT WORKING:
def merge_logs_files_from_all_processes():
    """
    Merge the logs rom all processes, logs that will be writen in this function wont be merged.
    """

    logs_files = [log.value for log in LogFilesTypes]  # For all log files

    for log_file_type in logs_files:
        log_pattern_for_globbing = log_file_path_pattern.format(suffix=log_file_type, pname="*")

        rows_from_all_files = []
        for current_file_name in glob(log_pattern_for_globbing):
            with open(current_file_name, 'r', encoding="utf-8") as current_file:
                # Add only none "\r\n" rows, and without leading \r\n
                rows_from_all_files.extend([row.lstrip() for row in current_file.read().split(logs_separator) if row.strip()])

        sorted_rows_by_date = sorted(rows_from_all_files, key=lambda row: parse_datetime(str(row).split("::")[0]))
        with open(os.path.join(get_logs_folder_for_this_process(), os.path.basename(log_pattern_for_globbing)), 'w',
                  encoding="utf-8") as merged_log_file:
            merged_log_file.write("\n".join(sorted_rows_by_date))
