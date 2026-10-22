import unittest

from brackets_validator import (
    BASIC_PAIRS,
    UnbalancedBracketsError,
    find_invalid_positions,
    highlight,
    validate,
)


class TestFindInvalidPositions(unittest.TestCase):
    def test_empty_string_is_valid(self):
        self.assertEqual(find_invalid_positions(""), [])

    def test_no_brackets_is_valid(self):
        self.assertEqual(find_invalid_positions("hello world"), [])

    def test_simple_valid(self):
        self.assertEqual(find_invalid_positions("(a)"), [])

    def test_nested_valid(self):
        self.assertEqual(find_invalid_positions("<a{b(c)}d>"), [])

    def test_extra_closing(self):
        self.assertEqual(find_invalid_positions("())"), [2])

    def test_unclosed_opening(self):
        self.assertEqual(find_invalid_positions("(()"), [0])

    def test_wrong_type(self):
        self.assertEqual(find_invalid_positions("(}"), [0, 1])

    def test_interleaved(self):
        self.assertEqual(find_invalid_positions("({)}"), [0, 2])

    def test_closing_first(self):
        self.assertEqual(find_invalid_positions(")("), [0, 1])

    def test_example_from_assignment(self):
        self.assertEqual(
            find_invalid_positions("<div><p>{ test }}</p</div>"), [16, 17]
        )

    def test_basic_pairs_ignore_other_brackets(self):
        self.assertEqual(find_invalid_positions("{<(a)", BASIC_PAIRS), [])
        self.assertEqual(find_invalid_positions("{<(a", BASIC_PAIRS), [2])


class TestValidate(unittest.TestCase):
    def test_valid_returns_empty_list(self):
        self.assertEqual(validate("(a{b}<c>)"), [])

    def test_raises_value_error_with_positions(self):
        with self.assertRaises(ValueError) as ctx:
            validate("<div><p>{ test }}</p</div>")
        self.assertEqual(
            str(ctx.exception), "Дужки незбалансовані на позиціях 16, 17"
        )

    def test_exception_exposes_positions(self):
        with self.assertRaises(UnbalancedBracketsError) as ctx:
            validate("())")
        self.assertEqual(ctx.exception.positions, [2])


class TestHighlight(unittest.TestCase):
    def test_carets_under_positions(self):
        self.assertEqual(highlight("())", [2]), "  ^")

    def test_example(self):
        text = "<div><p>{ test }}</p</div>"
        self.assertEqual(highlight(text, [16, 17]), " " * 16 + "^^")

    def test_tab_is_preserved(self):
        self.assertEqual(highlight("\t)", [1]), "\t^")


if __name__ == "__main__":
    unittest.main()
