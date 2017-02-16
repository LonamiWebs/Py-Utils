# primeseq
Simple `range()`-like iterator class used to find primes. Only `6n + 5±2`
primes are checked when generating the range, and only numbers up to the
square root are checked by using previously found primes.

Two versions are provided:
- `infprimeseq` is a non-stop iterator (avoids checking for an upper limit).
- `primeseq` is a convenient iterator which allows specifying an upper bound.
