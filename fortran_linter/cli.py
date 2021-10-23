import argparse
import itertools as it
import os
import pathlib
import sys
from typing import Optional, Sequence

from .main import LineChecker

GLOBS = ["*.f90", "*.f95"]


def _expand_files(file_or_dir):
    files = []
    if os.path.isdir(file_or_dir):
        path = pathlib.Path(file_or_dir)
        for glob in GLOBS:
            files.extend([str(p) for p in path.glob(glob)])
    else:
        files.append(file_or_dir)  # always return a collection
    return files


def parse_arguments(input_args: Optional[Sequence]):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "input",
        nargs="+",
        type=_expand_files,
        help=(
            "Input file(s) or directories.\n"
            "If the input is a directory all files with extension f90 and f95 are checked.",
        ),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i", "--inplace", action="store_true", help="Correct the errors inplace."
    )
    group.add_argument("--stdout", action="store_true", help="Output to stdout")
    group.add_argument(
        "--syntax-only",
        "--fsyntax-only",
        action="store_true",
        help="Print syntax errors to stdout. Default %(default)s.",
    )
    parser.add_argument(
        "--linelength", type=int, default=120, help="Line length. Default %(default)s."
    )
    parser.add_argument(
        "--max-errors",
        default=-1,
        type=int,
        help=(
            "Maximum number of errors to report. Set "
            "to -1 to deactivate. Default %(default)s"
        ),
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Be verbose.")

    args = parser.parse_args(input_args)

    return args


def main(input_args=None):
    args = parse_arguments(input_args)
    nerrors = 0

    files = it.chain(*args.input)  # here we flatten all the lists
    for ifile in set(files):
        if args.verbose:
            print(f"Checking {ifile}")
        lc = LineChecker(ifile, print_progress=False, linelen=args.linelength)

        nerrors += lc.errcount
        if args.syntax_only:
            if args.max_errors > 0:
                errs = lc.errors[: args.max_errors]
            else:
                errs = lc.errors
            print("\n".join(errs))
            continue

        if (args.stdout or args.inplace) and args.verbose:
            print(f"{lc.modifcount} modifications.")

        if args.stdout:
            print("".join(lc.corrected_lines))
        elif args.inplace:
            # Copy original file
            os.rename(ifile, ifile + ".orig")
            with open(ifile, "w") as f:
                f.writelines(lc.corrected_lines)

    if nerrors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
