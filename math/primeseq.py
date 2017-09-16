#!/usr/bin/python3
from bisect import bisect_left, bisect_right
from itertools import islice


def is_safe_prime(n):
    # safe version, this will always work
    if n < 2:
        return False
    if n < 4:
        return True

    if n % 2 == 0:
        return False
    for i in range(3, n, 2):
        if n % i == 0:
            return False

    return True


class primeseq:
    def __init__(self, initial_buffer_size=None):
        self._i = -1
        self._e = primeseq.eratosthenes()
        if initial_buffer_size:
            self._buffer = [next(self._e) for _ in range(initial_buffer_size)]
            self._buffersize = initial_buffer_size
        else:
            self._buffer = [next(self._e)]
            self._buffersize = 1

    def __iter__(self):
        self._i = -1
        return self

    def __next__(self):
        self._i += 1
        if self._i == self._buffersize:
            p = next(self._e)
            self._buffer.append(p)
            self._buffersize += 1
            return p
        else:
            return self._buffer[self._i]

    def __contains__(self, n):
        # Special cases
        if n < 4:
            if n < 2:
                return False
            return True

        # Fast check
        if ((n - 5) % 6 != 0) and ((n - 7) % 6 != 0):
            return False

        # Can this number be on the buffer?
        if n <= self._buffer[-1]:
            if n == self._buffer[-1]:
                # No need to use binary search at all
                return True

            # Binary search
            pos = bisect_left(self._buffer, n, 0, self._buffersize)
            return pos != self._buffersize and self._buffer[pos] == n

        # Not in the buffer, so increase it until we have enough primes
        # to check against n (we may not need to increase it at all)
        limit = int(n**0.5) + 1
        if self._buffer[-1] < limit:
            while self._buffer[-1] < limit:
                self._buffer.append(next(self._e))
            self._buffersize = len(self._buffer)
            # Had to expand until we had just enough, so last is the limit
            ilimit = self._buffersize
        else:
            # We had enough primes in the buffer, so find until which we
            # should be looking
            ilimit = bisect_right(self._buffer, limit)

        for p in islice(self._buffer, ilimit):
            if n % p == 0:
                return False

        # Nice, we have a new prime
        return True

    @staticmethod
    def eratosthenes():
        # Modified version from the second page:
        # archive.oreilly.com/pub/a/python/excerpt/pythonckbk_chap1/index1.html
        q = 3
        D = {}
        yield 2
        while True:
            p = D.pop(q, None)
            # Check 'if p' instead 'if p is None', which is around 15% faster.
            if p:
                # Used to be 'x = p + q', and then 'or x even' in the loop,
                # implemented as 'or not (x&1)'.
                #
                # We know that q is always odd, and p is q*q (where q is odd)
                # Multiplying an odd number by any other (or even itself) is
                # always odd. Adding two odds together is always even, so we
                # always need to add p again, or simply add 2p. ~30% speed-up.
                p2 = p * 2
                x = p2 + q
                while x in D:
                    x += p2
                D[x] = p
            else:
                yield q
                D[q*q] = q
            q += 2

    # Call infprimeseq.unwrap() for a faster iterator, but cannot be
    # reused, and checking whether it contains some element will fail.
    unwrap = eratosthenes


if __name__ == '__main__':
    print('Testing…')
    ps = primeseq()
    for i in range(0, 10000):
        if (i in ps) != is_safe_prime(i):
            if is_safe_prime(i):
                print(i, '\tshould     be prime, but is it in ps?:', i in ps)
            else:
                print(i, '\tshould not be prime, but is it in ps?:', i in ps)
    print('Test done.')
