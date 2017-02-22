# Logicmind
Very simple logic parser, used to find or test solutions for logical
expressions.

## Basic usage
It's most common usage is to find all the solutions to a given expression,
which can be achieved with the `-s` modifier. Solutions can be tested
manually with the `-t` modifier.

For example, if one wanted the following expression:

```A ↔ (B → ¬A)```

Can be solved by issuing any of the following:
```bash
python3 main.py -s "A <-> [B -> ¬A]"
python3 main.py -s "A ↔ B → ¬A"
python3 main.py -s "A ↔ {B -> !A)"
```

With the following output:
```bash
Found a single solution:
* A: 1
* B: 0
```

Note how one doesn't need to use `()`, any parenthesis can be used and
even combined (`(p -> q]` would be valid). One can also mix symbols like
`<->` and `→` without trouble.

For more help, check out `python3 main.py --help` or the source code itself.
