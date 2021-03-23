import logging
import re

logging.basicConfig(filename="myapp.log", level=logging.DEBUG)
re_strings = re.compile(r"([\"'])(?:\\\1|.)*?\1")


def to_lowercase(line: str, match):
    sub = line[match.start() : match.end()].lower()
    return line[: match.start()] + sub + line[match.end() :]


class FortranRules:
    rules = [
        # Fix "real*4" to "real(4)"
        # Need to be fixed before spaces around operators
        (r"({types})\*(\w+)", r"\1(\2)", "Use new syntax TYPE(kind)"),
        # Spaces in "do i = start, end"
        (r"do (\w+)=(\S+),(\S+)", r"do \1 = \2, \3", "Missing spaces"),
        # spaces around operators
        (r"(\w|\))({operators})", r"\1 \2", "Missing space before operator"),
        (r"({operators})(\w|\()", r"\1 \2", "Missing space after operator"),
        # " :: "
        (r"(\S)::", r"\1 ::", "Missing space before separator"),
        (r"::(\S)", r":: \1", "Missing space after separator"),
        # One should write "this, here" not "this,here"
        (r"({punctuations})(\w)", r"\1 \2", "Missing space after punctuation"),
        # should use lowercase for type definition
        (r"\b({types_upper})\s*::", to_lowercase, "Types should be lowercased"),
        # if (foo), ...
        (r"({structs})\(", r"\1 (", "Missing space before parenthesis"),
        # Should prepend "use omp_lib" by "!$" for portability
        (r"^(\s*)use omp_lib", "\1!$ use omp_lib", 'Should prepend with "!$"'),
        # Keep lines shorter than 80 chars
        (r"^.{linelen_re}.+$", None, "Line length > {linelen} characters"),
        # Convert tabulation to spaces
        (r"\t", "  ", "Should use 2 spaces instead of tabulation"),
        # Fix "foo! comment" to "foo ! comment"
        (r"(\w)\!", r"\1 !", "At least one space before comment"),
        # Fix "!bar" to "! bar"
        (r"\!(|\s\s+)(\S)", r"! \2", "Exactly one space after comment"),
        # Remove trailing ";"
        (r";\s*$", r"\n", 'Useless ";" at end of line'),
        [
            # Support preprocessor instruction
            (r"\#endif", None, None),
            (r"end(if|do|subroutine|function)", r"end \1", "Missing space after `end'"),
        ],
        [
            # Spaces around '='
            # Skip len=, kind=
            (r"\((kind|len)=", None, None),
            # Skip write statements
            (r"write\s*\(.*\)", None, None),
            # Skip open statements
            (r"open\s*\([^\)]+\)", None, None),
            # Skip lines defining variables
            ("::", None, None),
            # Match anything else
            (r'=(\w|\(|\.|\+|-|\'|")', r"= \1", 'Missing space after "="'),
        ],
        [
            # Spaces around '='
            # Skip len=, kind=
            (r"\((kind|len)=", None, None),
            # Skip write statements
            (r"write\s*\(.*\)", None, None),
            # Skip open statements
            (r"open\s*\([^\)]+\)", None, None),
            # Skip lines defining variables
            ("::", None, None),
            # Match anything else
            (r"(\w|\)|\.)=", r"\1 =", 'Missing space before "="'),
        ],
        # Trailing whitespace
        (r"( \t)+$", r"", "Trailing whitespaces"),
        # Kind should be parametrized
        (r"\(kind\s*=\s*\d\s*\)", None, 'You should use "sp" or "dp" instead'),
        # Use [] instead of \( \)
        (r"\(\\([^\)]*)\\\)", r"[\1]", 'You should use "[]" instead'),
        # OpenMP
        [
            # Remove lines starting with a !$
            (r"!\$", None, None),
            (
                r"(call |\w+ ?= ?|(?!\w))omp_",
                r"!$ \1",
                "Should prepend OpenMP calls with !$",
            ),
        ],
        # MPI
        (
            r'include ["\']mpif.h[\'"]',
            None,
            "Should use `use mpi_f08` instead (or `use mpi` if not available)",
        ),
    ]

    types = [r"real", r"character", r"logical", r"integer"]
    operators = [
        r"\.eq\.",
        r"\.neq\.",
        r"\.gt\.",
        r"\.lt\.",
        r"\.le\.",
        r"\.leq\.",
        r"\.ge\.",
        r"\.geq\.",
        r"==",
        r"/=",
        r"<=",
        r"<",
        r">=",
        r">",
        r"\.and\.",
        r"\.or\.",
        r"\+",
        r"\-",
        r"\*",
        r"\/",
    ]
    structs = [r"if", r"select", r"case", r"while"]
    punctuation = [",", r"\)", ";"]

    def __init__(self, linelen=120):
        self.linelen = linelen
        operators_re = r"|".join(self.operators)
        types_re = r"|".join(self.types)
        struct_re = r"|".join(self.structs)
        punctuation_re = r"|".join(self.punctuation)

        fmt = dict(
            operators=operators_re,
            types_upper=types_re.upper(),
            types=types_re,
            structs=struct_re,
            punctuations=punctuation_re,
            linelen_re="{%s}" % self.linelen,
            linelen=f"{self.linelen}",
        )

        newRules = [self.format_rule(rule, fmt) for rule in self.rules]
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


class LineChecker:
    def __init__(self, fname, print_progress=False, linelen=120):
        with open(fname) as f:
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
            meta = {
                "line": i + 1,
                "original_line": line.replace("\n", ""),
                "filename": self.filename,
            }

            line, _ = self.check_ruleset(line, line, meta, self.rules.get())
            self.corrected_lines.append(line)

    def check_ruleset(self, line, original_line, meta, ruleset, depth=0):
        if isinstance(ruleset, tuple):
            rule = ruleset
            line, hints = self.check_rule(line, original_line, meta, rule)
        else:
            for rule in ruleset:
                line, hints = self.check_ruleset(
                    line, original_line, meta, rule, depth + 1
                )
                # Stop after first match
                if hints > 0 and depth >= 1:
                    break

        return line, hints

    def check_rule(self, line, original_line, meta, rule):
        regexp, correction, msg = rule
        original_strings = [m[0] for m in re_strings.finditer(original_line)]
        comment_start = line.find("!")
        errs = 0
        hints = 0
        newLine = line
        for res in reversed(list(regexp.finditer(line))):
            corrected = newLine
            if 0 <= comment_start < res.start():
                # do not modify a comment
                # except if comment_start == res.start()
                # (adding space after first !)
                continue
            meta["pos"] = res.start() + 1
            hints += 1
            if callable(correction):
                self.modifcount += 1
                part = corrected[res.start() : res.end()]
                fix = correction(part, res)
                corrected = corrected[: res.start()] + fix + corrected[res.end() :]
            elif correction is not None:
                self.modifcount += 1
                part = corrected[res.start() : res.end()]
                fix = regexp.sub(correction, part)
                corrected = corrected[: res.start()] + fix + corrected[res.end() :]

            # Now check we haven't modified any string
            new_strings = [m[0] for m in re_strings.finditer(corrected)]
            if new_strings != original_strings:
                continue

            meta["pos"] = res.start() + 1
            hints += 1
            self.modifcount += 1
            meta["correction"] = newLine = corrected
            if msg is not None:
                self.fmt_err(msg, meta)
                errs += 1
                self.errcount += 1

        return newLine, hints

    def fmt_err(self, msg, meta):
        showpos = " " * (meta["pos"]) + "1"
        self.errors.append(
            (
                "{meta[filename]}:{meta[line]}:{meta[pos]}:\n\n"
                " {meta[original_line]}\n {showpos}\n"
                "Warning: {msg} at (1)."
            ).format(meta=meta, msg=msg, showpos=showpos)
        )
