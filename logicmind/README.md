# Logicmind
Very simple logic parser, used to find or test solutions for logical
expressions. The expressions must be well formed formulas and clearly
separated by the use of whitespaces, for example, the next would not be valid:
`A -> ¬B`; however, the following would be: `A -> (¬B)`.

Any parenthesis can be used to separate the formulas (`()`, `[]` and `{}` are
all treated equally).
