import logging
import re
from typing import Callable, Dict, Iterator, List, Optional, Tuple, Union

logging.basicConfig(filename="myapp.log", level=logging.DEBUG)
re_strings = re.compile(r"([\"']).*?\1")


def to_lowercase(line: str, match: re.Match) -> str:
    sub = line[match.start() : match.end()].lower()
    return line[: match.start()] + sub + line[match.end() :]


RAW_BASERULE_T = Tuple[
    str, Optional[Union[str, Callable[[str, re.Match], str]]], Optional[str]
]
RAW_RULE_T = Union[RAW_BASERULE_T, List[RAW_BASERULE_T]]
BASERULE_T = Tuple[
    re.Pattern, Optional[Union[str, Callable[[str, re.Match], str]]], Optional[str]
]
RULE_T = Union[BASERULE_T, List[BASERULE_T]]


class FortranRules:
    _rules: List[RAW_RULE_T] = [
        # Fix "real*4" to "real(4)"
        # Need to be fixed before spaces around operators
        (r"\b({types})\*(\w+)", r"\1(\2)", "Use new syntax TYPE(kind)"),
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
        (r"^(\s*)use omp_lib", r"\1!$ use omp_lib", 'Should prepend with "!$"'),
        # Keep lines shorter than 80 chars
        (r"^.{linelen_re}.+$", None, "Line length > {linelen} characters"),
        # Convert tabulation to spaces
        (r"\t", "  ", "Should use 2 spaces instead of tabulation"),
        # Fix "foo! comment" to "foo ! comment"
        (r"(\w)(\!(?!\$)|\!\$)", r"\1 \2", "At least one space before comment"),
        # Fix "!bar" to "! bar"
        (r"\!(|\s\s+)(?!\$)(\S)", r"! \2", "Exactly one space after comment"),
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
        # Replace .eq., .neq., .lt., .gt., etc. by their more explicit equivalent
        (r"\.eq\.", "==", "Replace .eq. with =="),
        (r"\.ne\.", "/=", "Replace .ne. with /="),
        (r"\.gt\.", ">", "Replace .gt. with >"),
        (r"\.geq\.", ">=", "Replace .geq. with >="),
        (r"\.lt\.", "<", "Replace .lt. with <"),
        (r"\.leq\.", "<=", "Replace .lt. with <="),
    ]

    rules: List[RULE_T]

    types = [r"real", r"character", r"logical", r"integer"]
    operators = [
        r"\.eq\.",
        r"\.ne\.",
        r"\.gt\.",
        r"\.lt\.",
        r"\.le\.",
        r"\.leq\.",
        r"\.ge\.",
        r"\.geq\.",
        r"\.eqv\.",
        r"==",
        r"/=",
        r"<=",
        r"<",
        r">=",
        r">",
        r"\.not\.",
        r"\.and\.",
        r"\.or\.",
        r"(?<!(?:\d|\.)[eEdD])\+",
        r"(?<!(?:\d|\.)[eEdD])\-",
        r"\*",
        r"\/",
    ]
    structs = [r"if", r"select", r"case", r"while"]
    punctuation = [",", r"\)", ";"]

    lineline: int

    def __init__(self, linelen: int = 120):
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

        self.rules = [self.format_rule(rule, fmt) for rule in self._rules]

    def get(self) -> List[RULE_T]:
        return self.rules

    def format_rule(self, rule: RAW_RULE_T, fmt: Dict) -> RULE_T:
        if isinstance(rule, tuple):
            rxp, replacement, msg = rule
            msg = msg.format(**fmt) if msg is not None else None
            regexp = re.compile(rxp.format(**fmt))
            return (regexp, replacement, msg)
        elif isinstance(rule, list):
            return [self.format_rule(r, fmt) for r in rule]  # type: ignore
        else:
            raise NotImplementedError


INDENTER_RULES = (
    re.compile(r"\b(if.*then|do|select|case|while|subroutine|function|module)\b"),
)
CONTINUATION_LINE_RULES = (re.compile(r"&"),)
DEDENTER_RULES = (
    re.compile(
        r"\b(end|endif|enddo|endselect|endcase|endwhile|endsubroutine|endfunction|endmodule)\b"
    ),
)
IMMEDIATE_DEDENTER_RULES = (
    re.compile(r"\b(contains|else)\b"),
    DEDENTER_RULES[0],
)
WHITESPACE_RULE = re.compile(
    r"^[^\S\r\n]*"
)  # match any whitespace, but not end-of-line
STRING_MARK_DETECTOR = re.compile(r"(?<!(?<!\\)\\)['\"]")
COMMENT_MARK_DETECTOR = re.compile(r"!")


def string_locations(line: str) -> Iterator[Tuple[int, int]]:
    """
    Return the locations of all strings in a line.
    """
    # Find all occurences of ' and "
    current_mark = None
    opening_loc = None
    for match in STRING_MARK_DETECTOR.finditer(line):
        mark = match.group(0)
        if current_mark is None:
            # Opening mark
            current_mark = mark
            opening_loc = match.start()
        elif mark == current_mark:
            # Closing mark
            current_mark = None
            yield opening_loc, match.end()
            opening_loc = None


def in_string(
    line: str, span: Tuple[int, int], string_spans: List[Tuple[int, int]]
) -> bool:
    """Check if a span is in a string.

    Parameters
    ----------
    line : str
        The line to check.
    span : Tuple[int, int]
        The span to check.

    Returns
    -------
    bool, True if the span if *fully* contained in a string
    """
    for start, end in string_spans:
        if start <= span[0] < span[1] < end:
            return True

    return False


def comment_location(line: str) -> int:
    """Check whether a line ends with a Fortran comment.

    Parameter
    ---------
    line: str
        The line to check.

    Returns
    -------
    int: location of the comment-opening character, len(line) if the line does not end with a comment.
    """
    if line.strip().startswith("#"):
        return line.index("#")

    string_spans = list(string_locations(line))
    # We find the location of all '!' and verify we are not in a string
    for match in COMMENT_MARK_DETECTOR.finditer(line):
        span = match.span()

        if not in_string(line, span, string_spans):
            return span[0]

    return len(line)


class Indenter:
    Nindent: int
    current_line_indent: int = 0
    continuation_line: bool = False

    def __init__(self, Nindent: int):
        self.Nindent = Nindent

    def checker(
        self,
        line: str,
        rules: Tuple[re.Pattern, ...],
        comment_pos: int,
        string_spans: List[Tuple[int, int]],
    ) -> bool:
        for rule in rules:
            for match in rule.finditer(line):
                span = match.span()
                if span[1] < comment_pos and not in_string(line, span, string_spans):
                    return True
        return False

    def indent_line(self, line: str) -> str:
        if line.startswith("#"):
            return line

        comment_pos = comment_location(line)
        next_line_indent = self.current_line_indent
        string_spans = list(string_locations(line))
        curline_continuation = False

        indent = False
        dedent = False
        if self.checker(line, DEDENTER_RULES, comment_pos, string_spans):
            dedent = True
        elif self.checker(line, INDENTER_RULES, comment_pos, string_spans):
            indent = True
        elif self.checker(line, CONTINUATION_LINE_RULES, comment_pos, string_spans):
            curline_continuation = True

        # If we were in a continuation line previously but are not anymore
        if not self.continuation_line and curline_continuation:
            indent = True
        elif self.continuation_line and not curline_continuation:
            dedent = True
        self.continuation_line = curline_continuation

        if self.checker(line, IMMEDIATE_DEDENTER_RULES, comment_pos, string_spans):
            cur_line_shift = self.Nindent

        else:
            cur_line_shift = 0

        if indent:
            next_line_indent += self.Nindent
        if dedent:
            next_line_indent = max(0, next_line_indent - self.Nindent)

        prefix = " " * max(0, self.current_line_indent - cur_line_shift)
        new_line = WHITESPACE_RULE.sub(prefix, line)
        self.current_line_indent = next_line_indent

        return new_line

    def __call__(self, lines: List[str]) -> List[str]:
        return [self.indent_line(line) for line in lines]


class LineChecker:
    filename: str
    original_lines: List[str]
    lines: List[str]
    corrected_lines: List[str]
    print_progress: bool
    rules: FortranRules
    indenter: Indenter
    errcount: int
    modifcount: int
    errors: List

    def __init__(
        self,
        fname: str,
        print_progress: bool = False,
        linelen: int = 120,
        indent_size: int = 4,
    ):
        with open(fname) as f:
            lines = f.readlines()
        self.filename = fname
        self.corrected_lines = []
        self.print_progress = print_progress

        self.rules = FortranRules(linelen=linelen)
        self.indenter = Indenter(Nindent=indent_size)

        self.errcount = 0
        self.modifcount = 0
        self.errors = []

        self.original_lines = lines

        # Indent the lines
        self.lines = self.indenter(lines)

        # Check the lines
        self.check_lines(self.original_lines, self.lines)

    def check_lines(self, original_lines: List[str], lines: List[str]) -> None:
        for i, (original_line, line) in enumerate(zip(original_lines, lines)):
            meta = {
                "line": i + 1,
                "original_line": original_line.replace("\n", ""),
                "filename": self.filename,
            }

            line, _ = self.check_ruleset(
                line, original_line=original_line, meta=meta, ruleset=self.rules.get()
            )
            self.corrected_lines.append(line)

    def check_ruleset(
        self,
        line: str,
        *,
        original_line: str,
        meta: Dict,
        ruleset: Union[RULE_T, List[RULE_T]],
        depth: int = 0,
    ) -> Tuple[str, int]:
        if isinstance(ruleset, tuple):
            return self.check_rule(
                line, original_line=original_line, meta=meta, rule=ruleset
            )

        for rule in ruleset:
            line, hints = self.check_ruleset(
                line,
                original_line=original_line,
                meta=meta,
                ruleset=rule,
                depth=depth + 1,
            )
            # Stop after first match
            if hints > 0 and depth >= 1:
                break

        return line, hints

    def check_rule(
        self, line: str, *, original_line: str, meta: Dict, rule: BASERULE_T
    ) -> Tuple[str, int]:
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

    def fmt_err(self, msg: str, meta: Dict) -> None:
        showpos = " " * (meta["pos"]) + "1"
        self.errors.append(
            (
                "{meta[filename]}:{meta[line]}:{meta[pos]}:\n\n"
                " {meta[original_line]}\n {showpos}\n"
                "Warning: {msg} at (1)."
            ).format(meta=meta, msg=msg, showpos=showpos)
        )
