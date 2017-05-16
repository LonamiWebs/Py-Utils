math
====
Several math-related utilities. Almost everything from here is inspired
by problems or useful algorithms I required on my university's lectures.


euler
-----
The Euler's totient function (also known as the *Euler phi function*), also
expressed as φ(n). This functions gives the amount of numbers below 'n' which
are coprime with n (e.g., the `gcd(a, n) = 1`, meaning no other number greater
than 1 actually divides them).


extrapolate
-----------
Extrapolation technique using difference trees (although not only difference
trees actually, division or any other combination of operators can be used)
to infer the next value. The site from which I found this can be seen
[here](http://alteredqualia.com/visualization/hn/sequence/).


extrapolate_basic
-----------------
First version of `extrapolate.py`, with the operations hardcoded.


newton_polynomial
-----------------
An implementation for the
[Newton's polynomial](https://en.wikipedia.org/wiki/Newton_polynomial),
extensively explained on the source code itself.


polynomials
-----------
Includes the Ruffini's rule and a method to visualize the process, as well
as for (trying to) finding integer roots of arbitrary polynomial known its
quotients. Useful to factorize arbitrary polynomials.


primeseq
--------
Simple `range()`-like iterator class used to find primes. Only `6n + 5±2`
primes are checked when generating the range, and only numbers up to the
square root are checked by using previously found primes.

Two versions are provided:
* `infprimeseq` is a non-stop iterator (avoids checking for an upper limit).
* `primeseq` is a convenient iterator which allows specifying an upper bound.
