import os
import argparse

import nelson.gtomscs as nelson

from glob import glob

COURSE = "cs6475"
SETTINGS = {'finalproject': {"finalproject": {"size": 6, "ext": ["pdf"]}}}

LATE_POLICY = """Late Policy:\n
  \"I have read the late policy for CS6475. I understand that only my last
  commit before the late submission deadline will be accepted and that late
  penalties apply if any part of the assignment is submitted late.\"
"""

HONOR_PLEDGE = """Honor Pledge:\n
  \"I have neither given nor received aid on this assignment.\"
"""


def require_pledge(policy_text):
    print(policy_text)
    ans = raw_input("Please type 'yes' to agree and continue>")
    if ans != "yes":
        raise RuntimeError(
            "You accept all policies before submitting your assignment.")
    print


def validate_file_info(pattern, lo=1, hi=1, size=6, ext=[]):

    filenames = [x for x in glob(pattern + ".*")
                 if not ext or str.lower(os.path.splitext(x)[-1])[1:] in ext]

    if not (lo <= len(filenames) <= hi):
        raise RuntimeError(
            ("Submission Failed - you are required to submit at least {!s} " +
             "files and no more than {!s} files that match the pattern " +
             "'{!s}.<EXT>' with one of the allowed extensions: {!s}. You " +
             "submitted only {!s}")
            .format(lo, hi, pattern, ext, len(filenames)))

    large_files = [x for x in filenames if os.stat(x).st_size > size * 2**20]
    if large_files:
        raise RuntimeError(
            ("Submission Failed: One or more files is too large. Please " +
             "make sure that the following files are under {!s}MB and try " +
             "again: {!s}").format(size, large_files))

    return filenames


def main(args):

    require_pledge(LATE_POLICY)
    require_pledge(HONOR_PLEDGE)

    required_files = [validate_file_info(ptn, **kwargs)
                      for ptn, kwargs in SETTINGS.get(args.quiz, {}).items()]
    additional_files = map(glob, args.filenames)
    filenames = reduce(list.__add__, required_files + additional_files, [])

    nelson.submit(COURSE, args.quiz, filenames, environment=args.environment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Submit assignment to the Bonnie.')
    parser.add_argument(
        'quiz', choices=SETTINGS.keys(),
        help="Select the name of the quiz to submit")
    parser.add_argument(
        '-f', '--filenames', nargs="+", default=[],
        help="The names of any additional files to submit.")
    parser.add_argument(
        '-e', '--environment', default='production',
        choices=['local', 'development', 'staging', 'production'],
        help="Select the server to use (default: production)")
    args = parser.parse_args()

    main(args)
