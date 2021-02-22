"""
Lint all python files before they are committed based upon pylinter
"""

import subprocess
import re
from pylint.lint import Run

LINTER_THRESHOLD = 8.0
EVALUATION_CHECK_PASS = "NO_PYLINT_EVALUATION"

FILE_NAME_TYPES_TO_IGNORE_FOR_EVALUATION = [
    "_auto_", "setup.py", "manage.py", "urls", "conf.py"]
FILE_NAME_STARTS_TO_IGNORE_FOR_EVALUATION = ["settings", "constants"]


def get_committed_files():
    """
    Gets the list of files alongwith the paths of the files present in the commit
    """
    files = []
    files_list = bash_command(
        'git', 'diff', '--cached', '--name-status').split()
    for i in range(0, len(files_list), 2):
        action = files_list[i].decode("utf-8")
        file = files_list[i + 1].decode("utf-8")
        if action != 'D' and file.endswith('.py'):
            files.append(file)
    return files


def stop_commit_process(invalid_file):
    """
    The method is used to stop the commit process for the files
    :param invalid_file: File whose linting is incorrect
    """
    raise Exception(
        f"Evaluation score for {invalid_file} is less than {LINTER_THRESHOLD}")


def bash_command(*args, **kwargs):
    """
    Run bash command.
    """
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, _ = proc.communicate()
    return out


def run_linter(linter_to_run_file):
    """
    Runs the linter for the file to be committed, and returns the linter score
    :param linter_to_run_file: Filename to be committed
    """
    if not check_if_file_to_evaluate(linter_to_run_file):
        return 10.0
    results = Run([linter_to_run_file], do_exit=False)
    return results.linter.stats['global_note']


def check_if_file_to_evaluate(file_location):
    """
    Checks whether the file refers to a constant not meant to be verified
    Any python file to skip evaluation should have "# NO_PYLINT_EVALUATION"
    in the first line
    :param file_location: Location of the file
    """
    try:
        file_name = file_location.split("/")[-1]
        if any(re.search(name_wildcard, file_name)
               for name_wildcard in FILE_NAME_TYPES_TO_IGNORE_FOR_EVALUATION):
            return False
        if any(re.match(start_wildcard, file_name)
               for start_wildcard in FILE_NAME_STARTS_TO_IGNORE_FOR_EVALUATION):
            return False
        with open(file_location, 'r') as f:
            l = f.read().split(" ")
            return l[1] != EVALUATION_CHECK_PASS
    except IndexError:
        return False


def auto_format_code(to_format_file):
    """
    Autoformats the file, which is being committed
    """
    bash_command('autopep8', '--in-place', '--aggressive',
                 '--aggressive', to_format_file)


def add_autoformatted_file(to_add_file):
    """
    git add the file that was auto-formatted
    """
    bash_command('git', 'add', to_add_file)


if __name__ == '__main__':
    files = get_committed_files()

    for file in files:
        auto_format_code(file)
        add_autoformatted_file(file)
        linter_score = run_linter(file)
        if linter_score < LINTER_THRESHOLD:
            stop_commit_process(file)
