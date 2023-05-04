import os
import logging
from argparse import ArgumentParser

from .utils import search_files_by_extension, filter_congruent_coverage_files, run_gcov


LOGGER = logging.getLogger("GcovReporter")


GCDA_FILE_EXT = ".gcda"
GCNO_FILE_EXT = ".gcno"

GCOV_FLAGS = ["--json-format"]


class InvokingGcovException(Exception):
    pass


class NoFilesFoundException(Exception):
    pass


def setup_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="GcovReporter",
        description="Creates summarized coverage reports created by gcov",
    )

    parser.add_argument(
        "path",
        help="Path where to run gcov reporter. Should match path where compiler invoked",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Run in debug mode", default=False
    )

    return parser


def main():
    # Setting up argument parser and aprsing args
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Enable debug mode if verbose flag is set
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Check if path argument is set, otherwise set cwd
    path = args.path
    if path is None:
        path = os.getcwd()

    # Search coverage files and exit if no files are found
    coverage_files = search_files_by_extension(
        search_path=path, extensions=(GCDA_FILE_EXT, GCNO_FILE_EXT)
    )
    if len(coverage_files) < 1:
        LOGGER.info("No files found. Exiting")
        exit(1)

    # Filter coverage files
    filtered_coverage_files = filter_congruent_coverage_files(coverage_files)

    # Invoke gcov
    try:
        run_gcov(filtered_coverage_files, GCOV_FLAGS, path)
    except:
        LOGGER.error("Error while invoking GCOV. Exiting")
        exit(1)

    # Parse gcovs json output


if __name__ == "__main__":
    main()
