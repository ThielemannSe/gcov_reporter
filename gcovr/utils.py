import os
import logging
from subprocess import Popen, PIPE
from typing import Tuple, Optional, List


LOGGER = logging.getLogger("GcovReporter")


def run_gcov(
    files: List[str], args: Optional[List[str]] = [], cwd: str | None = os.getcwd()
) -> None:
    """Executes gcov in a specified directory

    Args:
        files (List[str]): Coverage data files passed to gcov
        flags (List[str], optional): List of args passed to gcov. Defaults to [].
        cwd (str, optional): Working dir from where to invoke gcov
    Raises:
        RuntimeError: In case gcov exit code is not equal to 0. Defaults to os.getcwd()
    """

    process = Popen(["gcov"] + args + files, stdout=PIPE, stderr=PIPE, cwd=cwd)

    out, err = process.communicate()  # TODO logging

    if process.returncode != 0:
        raise RuntimeError(f"GCOV exited with returncode {process.returncode}. {err}")


def search_files_by_extension(
    search_path: str,
    extensions: Tuple[str],
    exclude_dirs: Optional[List[str]] = [],
) -> List[str]:
    """Searches for files with specific extension

    Args:
        search_path (str): path to start search from
        extensions (Iterable[str]): file extensions to be searched for
        exclude_dirs (Optional[List[str]], optional): directories to be excluded. Defaults to None.

    Returns:
        List[str]: All files found meeting requierements
    """
    LOGGER.info(f"Scanning directory {search_path}")

    coverage_files = []
    for root, dirs, files in os.walk(search_path, topdown=True):
        # TODO: should work for both relative and absolute paths not just for directory names
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith(extensions):
                coverage_files.append(root + "/" + file)

    if len(coverage_files) > 0:
        LOGGER.info(
            "Found {} files:\n\t{}".format(
                len(coverage_files), "\n\t".join(coverage_files)
            )
        )

    return coverage_files


def filter_congruent_coverage_files(files: List[str]) -> List[str]:
    """Filters coverage files if both .gcda and .gcno file exists
    for a file stem. .gcda file is always preferred. In case only .gcno
    file exists it is returned

    Args:
        files (List[str]): List of files to be filtered

    Returns:
        List[str]: Filtered list of files
    """
    selected_files = {}

    for file in files:
        stem, ext = os.path.splitext(file)

        if stem not in selected_files:
            selected_files[stem] = ext
            continue

        if ext == ".gcda":
            selected_files[stem] = ext

    return [stem + ext for stem, ext in selected_files.items()]
