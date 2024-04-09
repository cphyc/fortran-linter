from fortran_linter.main import comment_location, string_locations


def test_string_detection():
    answers = (
        ("print*, 'foo', 'bar', 'baz'", ((8, 13), (15, 20), (22, 27))),
        ('print*, "foo", "bar", "baz"', ((8, 13), (15, 20), (22, 27))),
        ("'test\\'", ((0, 7),)),
    )

    for s, exp_positions in answers:
        for pos, exp_pos in zip(string_locations(s), exp_positions, strict=False):
            assert pos == exp_pos


def test_hashtag_detection():
    comment_lines = (
        ("# test", 0),
        ("    #test", 4),
    )

    no_comment_lines = (
        r'"# character in a string"',
        r"'# character in a string'",
        r"'there', 'are', 'many', 'strings', 'here', '#'",
    )

    for line, icomment in comment_lines:
        assert comment_location(line) == icomment

    for line in no_comment_lines:
        assert comment_location(line) == len(line)


def test_fortran_comment_detection():
    comment_lines = (
        ("! test", 0),
        ("    !test", 4),
        ("'Contains a string', ! and a comment", 21),
        ("!! test", 0),
        ("    !!test", 4),
        ("'Contains a string', !! and a comment", 21),
        ("!> test", 0),
        ("    !>test", 4),
        ("'Contains a string', !> and a comment", 21),
    )

    no_comment_lines = (
        '"! character in a string"',
        "'! character in a string'",
        "'there', 'are', 'many', 'strings', 'here', '!'",
        "'test\\'!'",
    )

    for line, icomment in comment_lines:
        assert comment_location(line) == icomment

    for line in no_comment_lines:
        assert comment_location(line) == len(line)
