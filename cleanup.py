import re
import logging
logging.basicConfig(filename='myapp.log', level=logging.DEBUG)


class FortranRules(object):
    rules = [
        ('(\S)({operators})(\S)', r'\1 \2 \3',
         'Missing spaces around operator'),
        ('(\S)::(\S)|(\S)::(\s)|(\s)::(\S)', r'\1 :: \2',
         'Missing spaces around separator'),
        ('({ponctuations})(\w)', r'\1 \2',
         'Missing space after ponctuation'),
        ('({types_upper})', None,
         'Types should be lowercased'),
        ('({structs})\(', r'\1 (',
         'Missing parenthesis'),
        ('include ["\']mpif.h[\'"]', None,
         'Should use "use mpi" instead'),
        ('^(\s*)use omp_lib', '\1!$ use omp_lib',
         'Should prepend with "!$"')
    ]

    types = [r'real', r'character', r'logical', r'integer']
    operators = [r'\.eq\.', r'\.neq\.', r'\.gt\.', r'\.lt\.', r'\.leq\.',
                 r'\.geq\.', r'==', r'/=', '>', r'<',
                 r'<=', r'>=', '\.and\.', '\.or\.']
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
            print(regexp)
        self.rules = newRules

    def get(self):
        return self.rules


class LineChecker(object):
    def __init__(self, lines, do_correction=False):
        self.lines = lines
        self.corrected_lines = []

        self.rules = FortranRules()

        self._do_correction = do_correction
        self.check_lines()

    def check_lines(self):
        for i, line in enumerate(self.lines):
            meta = {'line': i}
            self.corrected_lines.append(self.check_not_ok(line, meta))

    def check_not_ok(self, line, meta):
        '''
        Check the line against the not ok rule.
        '''
        original_line = line
        for regexp, correction, msg in self.rules.get():
            # logging.debug('Testing %s' % regexp)
            # print('Testing %s on %s' % (regexp, line))
            res = regexp.search(original_line)
            if res:
                meta['pos'] = res.start()

                if correction is None:
                    newLine = line
                else:
                    newline = regexp.sub(correction, line)
                meta['correction'] = newline
                line = newline
                self.print_err(msg, meta)
        return line

    def print_err(self, msg, meta):
        print("{err} @ {meta[line]}:{meta[pos]}".format(err=msg, meta=meta))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input', help='Input file')
    parser.add_argument('-i', '--inplace', action='store_true',
                        help='Try to correct the errors inplace.')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        lc = LineChecker(f.readlines())

    if args.inplace:
        # with open(args.input + '.new', 'w') as f:
        print(''.join(lc.corrected_lines))


if __name__ == '__main__':
    main()
