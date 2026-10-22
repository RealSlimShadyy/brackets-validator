import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from brackets_validator.cli import main


class TestCli(unittest.TestCase):
    def run_main(self, user_input):
        out = io.StringIO()
        with patch("builtins.input", return_value=user_input) as mocked, \
                redirect_stdout(out):
            try:
                main()
            finally:
                mocked.assert_called_once_with("Введіть строку: ")
        return out.getvalue()

    def test_valid_string(self):
        self.assertEqual(self.run_main("(a)"), "Строка валідна\n")

    def test_invalid_string_raises_and_highlights(self):
        out = io.StringIO()
        with patch("builtins.input", return_value="())"), redirect_stdout(out):
            with self.assertRaises(ValueError) as ctx:
                main()
        self.assertEqual(
            str(ctx.exception), "Дужки незбалансовані на позиціях 2"
        )
        self.assertEqual(out.getvalue(), "())\n  ^\n")


if __name__ == "__main__":
    unittest.main()
