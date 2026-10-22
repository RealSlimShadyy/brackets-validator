# brackets-validator

Перевіряє, чи правильно закриті дужки `()`, `{}` та `<>` у рядку.

```
$ brackets-validator
Введіть строку: <div><p>{ test }}</p</div>
<div><p>{ test }}</p</div>
                ^^
ValueError: Дужки незбалансовані на позиціях 16, 17
```

Позиції рахуються з нуля. Як бібліотека:

```python
from brackets_validator import validate, UnbalancedBracketsError

validate("(a{b}<c>)")        # [] - все гаразд
validate("(a", pairs={"(": ")"})  # raises UnbalancedBracketsError (підклас ValueError)
```
