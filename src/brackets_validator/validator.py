"""Перевірка балансу дужок за допомогою стека (list)."""

BASIC_PAIRS = {"(": ")"}
ADVANCED_PAIRS = {"(": ")", "{": "}", "<": ">"}


class UnbalancedBracketsError(ValueError):
    """Дужки незбалансовані. Позиції (з нуля) зберігаються в .positions."""

    def __init__(self, positions):
        self.positions = list(positions)
        shown = ", ".join(str(p) for p in self.positions)
        super().__init__(f"Дужки незбалансовані на позиціях {shown}")


def find_invalid_positions(text, pairs=ADVANCED_PAIRS):
    """Повертає відсортований список індексів хибних дужок (порожній - все ок).

    Закриваюча дужка без пари (або не того типу) хибна сама по собі;
    відкриваючі, що залишились у стеку в кінці, теж хибні.
    """
    closers = set(pairs.values())
    stack = []  # елементи: (відкриваюча дужка, індекс)
    invalid = []
    for index, char in enumerate(text):
        if char in pairs:
            stack.append((char, index))
        elif char in closers:
            if stack and pairs[stack[-1][0]] == char:
                stack.pop()
            else:
                invalid.append(index)
    invalid.extend(index for _, index in stack)
    return sorted(invalid)


def validate(text, pairs=ADVANCED_PAIRS):
    """Піднімає UnbalancedBracketsError (ValueError), якщо дужки хибні."""
    invalid = find_invalid_positions(text, pairs)
    if invalid:
        raise UnbalancedBracketsError(invalid)
    return invalid


def highlight(text, positions):
    """Рядок зі знаками ^ під хибними дужками (табуляції зберігаються)."""
    marks = set(positions)
    line = "".join(
        "^" if i in marks else ("\t" if ch == "\t" else " ")
        for i, ch in enumerate(text)
    )
    return line.rstrip()
