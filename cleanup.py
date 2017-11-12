import re
import logging
import os
import sys

logging.basicConfig(filename='myapp.log', level=logging.DEBUG)


class FortranRules(object):
    rules = [
        (r'(\S)({operators})(\S)', r'\1 \2 \3',
         'Missing spaces around operator'),

        (r'(\S)::(\S)', r'\1 :: \2',
         'Missing spaces around separator'),

        (r'({ponctuations})(\w)', r'\1 \2',
         'Missing space after ponctuation'),

        (r'({types_upper})', None,
         'Types should be lowercased'),

        (r'({structs})\(', r'\1 (',
         'Missing parenthesis'),

        (r'include ["\']mpif.h[\'"]', None,
         'Should use "use mpi" instead'),

        (r'^(\s*)use omp_lib', '\1!$ use omp_lib',
         'Should prepend with "!$"'),

        (r'^.{{80}}.+$', None, 'Line length > 80 characters.'),

        (r'\t', '  ', 'Should use 2 spaces instead of tabulation'),

        (r'({types})\*(\w+)', r'\1(\2)', 'Use new syntax TYPE(kind)'),

        (r'(\w)\!', r'\1 !', 'At least one space before comment'),

        (r'\!(|\s\s+)(\w)', r'! \2', 'Exactly one space after comment'),

        (r';(\s*)?$', r'', 'Useless ";" at end of line'),

        (r'(?<!#)end(if|do|subroutine|function)', r'end \1',
         'Missing space after end')

    ]

    types = [r'real', r'character', r'logical', r'integer']
    operators = [r'\.eq\.', r'\.neq\.', r'\.gt\.', r'\.lt\.', r'\.leq\.',
                 r'\.geq\.', r'==', r'/=', r'<=', r'<',
                 r'>=', r'>', r'\.and\.', r'\.or\.']
    structs = [r'if', r'select', r'case', r'while']
    ponctuation = [',', '\)', ';']

    def __init__(self):
        operators_re = r'|'.join(self.operators)
        types_re = r'|'.join(self.types)
        struct_re = r'|'.join(self.structs)
        ponctuation_re = r'|'.join(self.ponctuation)

        fmt = dict(
            operators=operators_re,
            types_upper=types_re.upper(),
            types=types_re,
            structs=struct_re,
            ponctuations=ponctuation_re)
        newRules = []
        for rxp, replacement, msg in self.rules:
            regexp = re.compile(rxp.format(**fmt))
            newRules.append((regexp, replacement, msg))
        self.rules = newRules

    def get(self):
        return self.rules


class LineChecker(object):
    def __init__(self, fname):
        with open(fname, 'r') as f:
            lines = f.readlines()
        self.filename = fname
        self.lines = lines
        self.corrected_lines = []

        self.rules = FortranRules()

        self.errcount = 0
        self.errors = []

        # Check the lines
        self.check_lines()

    def check_lines(self):
        for i, line in enumerate(self.lines):
            meta = {'line': i + 1,
                    'filename': self.filename}
            self.corrected_lines.append(self.check_not_ok(line, meta))

    def check_not_ok(self, line, meta):
        '''
        Check the line against the not ok rule.
        '''
        original_line = line
        meta['original_line'] = line.replace('\n', '')
        for regexp, correction, msg in self.rules.get():
            for res in regexp.finditer(original_line):
                meta['pos'] = res.start() + 1
                if correction is None:
                    newLine = line
                else:
                    newLine = regexp.sub(correction, line)
                meta['correction'] = newLine
                line = newLine
                self.fmt_err(msg, meta)
                self.errcount += 1
        return line

    def fmt_err(self, msg, meta):
        showpos = ' '*(meta['pos']) + '1'
        self.errors.append((
            "{meta[filename]}:{meta[line]}:{meta[pos]}:\n\n"
            " {meta[original_line]}\n {showpos}\n"
            "Error: {msg} at (1)").format(
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

    args = parser.parse_args()

    nerrors = 0
    for ifile in set(args.input):
        lc = LineChecker(ifile)

        nerrors += lc.errcount
        if args.syntax_only:
            print('\n'.join(lc.errors))
            continue

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
