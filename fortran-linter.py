#!/usr/bin/env python
import re
import logging
import os
import sys

logging.basicConfig(filename='myapp.log', level=logging.DEBUG)


class FortranRules(object):
    rules = [
        # Spaces in "do i = start, end"
        (r'do (\w+)=(\S+),(\S+)', r'do \1 = \2, \3',
         'Missing spaces'),

        [
            # spaces around operators
            (r'(\w|\))({operators})(\w|\()', r'\1 \2 \3',
             'Missing spaces around operator'),
            (r'(\w|\))({operators})', r'\1 \2',
             'Missing space before operator'),
            (r'({operators})(\w|\()', r'\1 \2',
             'Missing space after operator')
        ],
        [
            # " :: "
            (r'(\S)::(\S)', r'\1 :: \2',
             'Missing spaces around separator'),
            (r'(\S)::', r'\1 ::',
             'Missing space before separator'),
            (r'::(\S)', r':: \1',
             'Missing space after separator')
        ],

        # One should write "this, here" not "this,here"
        (r'({ponctuations})(\w)', r'\1 \2',
         'Missing space after ponctuation'),

        # should use lowercase for type definition
        (r'\b({types_upper})\b', None,
         'Types should be lowercased'),

        # if (foo), ...
        (r'({structs})\(', r'\1 (',
         'Missing space before parenthesis'),

        # Use "use mpi" instead of depreciated "include mpif.h"
        (r'include ["\']mpif.h[\'"]', None,
         'Should use "use mpi" instead'),

        # Should prepend "use omp_lib" by "!$" for portability
        (r'^(\s*)use omp_lib', '\1!$ use omp_lib',
         'Should prepend with "!$"'),

        # Keep lines shorter than 80 chars
        (r'^.{linelen_re}.+$', None, 'Line length > {linelen} characters'),

        # Convert tabulation to spaces
        (r'\t', '  ', 'Should use 2 spaces instead of tabulation'),

        # Fix "real*4" to "real(4)"
        (r'({types})\*(\w+)', r'\1(\2)', 'Use new syntax TYPE(kind)'),

        # Fix "foo! comment" to "foo ! comment"
        (r'(\w)\!', r'\1 !', 'At least one space before comment'),

        # Fix "!bar" to "! bar"
        (r'\!(\w)', r'! \1', 'Exactly one space after comment'),

        # Remove trailing ";"
        (r';\s*$', r'\n', 'Useless ";" at end of line'),

        [
            # Support preprocessor instruction
            (r'\#endif', None, None),
            (r'end(if|do|subroutine|function)', r'end \1',
             'Missing space after `end\''),
        ],
        [
            # Spaces around '='
            ('(\(kind|\(len)=', None, None),  # skip len=, kind=
            (r'(?<!(\(kind|.\(len))=(\w|\(|\.|\+|-|\'|")', r' = \2',
             'Missing spaces around "="'),
        ],

        # Trailing whitespace
        (r'( \t)+$', r'', 'Trailing whitespaces'),

        # Kind should be parametrized
        (r'\(kind\s*=\s*\d\s*\)', None, 'You should use "sp" or "dp" instead'),

        # Use [] instead of \( \)
        (r'\(\\([^\)]*)\\\)', r'[\1]', 'You should use "[]" instead'),
    ]

    types = [r'real', r'character', r'logical', r'integer']
    operators = [r'\.eq\.', r'\.neq\.', r'\.gt\.', r'\.lt\.', r'\.leq\.',
                 r'\.geq\.', r'==', r'/=', r'<=', r'<',
                 r'>=', r'>', r'\.and\.', r'\.or\.']
    structs = [r'if', r'select', r'case', r'while']
    ponctuation = [',', '\)', ';']

    def __init__(self, linelen=120):
        self.linelen = linelen
        operators_re = r'|'.join(self.operators)
        types_re = r'|'.join(self.types)
        struct_re = r'|'.join(self.structs)
        ponctuation_re = r'|'.join(self.ponctuation)

        fmt = dict(
            operators=operators_re,
            types_upper=types_re.upper(),
            types=types_re,
            structs=struct_re,
            ponctuations=ponctuation_re,
            linelen_re="{%s}" % self.linelen,
            linelen="%s" % self.linelen)

        newRules = []
        for rule in self.rules:
            newRules.append(self.format_rule(rule, fmt))
        self.rules = newRules

    def get(self):
        return self.rules

    def format_rule(self, rule, fmt):
        if isinstance(rule, tuple):
            rxp, replacement, msg = rule
            msg = msg.format(**fmt) if msg is not None else None
            regexp = re.compile(rxp.format(**fmt))
            return (regexp, replacement, msg)
        elif isinstance(rule, list):
            return [self.format_rule(r, fmt) for r in rule]
        else:
            raise NotImplementedError


class LineChecker(object):
    def __init__(self, fname, print_progress=False, linelen=120):
        with open(fname, 'r') as f:
            lines = f.readlines()
        self.filename = fname
        self.lines = lines
        self.corrected_lines = []
        self.print_progress = print_progress

        self.rules = FortranRules(linelen=linelen)

        self.errcount = 0
        self.modifcount = 0
        self.errors = []

        # Check the lines
        self.check_lines()

    def check_lines(self):
        for i, line in enumerate(self.lines):
            meta = {'line': i + 1,
                    'original_line': line.replace('\n', ''),
                    'filename': self.filename}

            line, _ = self.check_ruleset(line, line, meta, self.rules.get())
            self.corrected_lines.append(line)

    def check_ruleset(self, line, original_line, meta, ruleset, depth=0):
        if isinstance(ruleset, tuple):
            rule = ruleset
            line, hints = self.check_rule(
                line, original_line, meta, rule)
        else:
            for rule in ruleset:
                line, hints = self.check_ruleset(
                    line, original_line, meta, rule, depth+1)
                # Stop after first match
                if hints > 0 and depth >= 1:
                    break

        return line, hints

    def check_rule(self, line, original_line, meta, rule):
        regexp, correction, msg = rule
        errs = 0
        hints = 0
        newLine = line
        for res in regexp.finditer(original_line):
            meta['pos'] = res.start() + 1
            hints += 1
            if correction is not None:
                self.modifcount += 1
                newLine = regexp.sub(correction, newLine)

            meta['correction'] = newLine
            if msg is not None:
                self.fmt_err(msg, meta)
                errs += 1
                self.errcount += 1

        return newLine, hints

    def fmt_err(self, msg, meta):
        showpos = ' '*(meta['pos']) + '1'
        self.errors.append((
            "{meta[filename]}:{meta[line]}:{meta[pos]}:\n\n"
            " {meta[original_line]}\n {showpos}\n"
            "Warning: {msg} at (1).").format(
                   meta=meta, msg=msg,
                   showpos=showpos
        ))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input', help='Input file(s)', nargs='+')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--inplace', action='store_true',
                       help='Correct the errors inplace.')
    group.add_argument('--stdout', action='store_true',
                       help='Output to stdout')
    group.add_argument('--syntax-only', action='store_true',
                       help='Print syntax errors to stdout')

    parser.add_argument('--linelength', type=int, default=120,
                        help='Line length')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Be verbose.')

    args = parser.parse_args()

    nerrors = 0
    for ifile in set(args.input):
        if args.verbose:
            print('Checking %s' % ifile)
        lc = LineChecker(ifile, print_progress=False, linelen=args.linelength)

        nerrors += lc.errcount
        if args.syntax_only:
            print('\n'.join(lc.errors))
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
