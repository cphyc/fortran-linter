from .main import LineChecker
import os
import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input', help='Input file(s)', nargs='+')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--inplace', action='store_true',
                       help='Correct the errors inplace.')
    group.add_argument('--stdout', action='store_true',
                       help='Output to stdout')
    group.add_argument('--syntax-only', '--fsyntax-only', action='store_true',
                       help='Print syntax errors to stdout. Default %(default)s.')
    parser.add_argument('--linelength', type=int, default=120,
                        help='Line length. Default %(default)s.')
    parser.add_argument('--max-errors', default=-1, type=int,
                        help=('Maximum number of errors to report. Set '
                              'to -1 to deactivate. Default %(default)s'))
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Be verbose.')

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()
    nerrors = 0
    for ifile in set(args.input):
        if args.verbose:
            print('Checking %s' % ifile)
        lc = LineChecker(ifile, print_progress=False, linelen=args.linelength)

        nerrors += lc.errcount
        if args.syntax_only:
            if args.max_errors > 0:
                errs = lc.errors[:args.max_errors]
            else:
                errs = lc.errors
            print('\n'.join(errs))
            continue

        if (args.stdout or args.inplace) and args.verbose:
            print('%s modifications.' % lc.modifcount)

        if args.stdout:
            print(''.join(lc.corrected_lines))
        elif args.inplace:
            # Copy original file
            os.rename(ifile, ifile + '.orig')
            with open(ifile, 'w') as f:
                f.writelines(lc.corrected_lines)

    if nerrors > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
