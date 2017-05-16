#!/usr/bin/python3


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


class infprimeseq:
    def __init__(self, initial_buffer_size=None):
        self.i = -1
        self.buffer = [2, 3, 5]

        if initial_buffer_size:
            if initial_buffer_size < 0:
                raise ValueError('initial_buffer_size must be a positive integer.')

            # Extend the buffer up to initial_buffer_size
            for i in range(initial_buffer_size):
                self.__next__()

            # Reset the internal stepper
            self.i = -1

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1

        # self.i should always be ≤ len(self.buffer), or someone messed with i
        if self.i >= len(self.buffer):
            # Prime numbers ≥ 5 satisfy either of the following:
            #   (n - 5) % 6 == 0
            #   (n - 7) % 6 == 0
            # If the first condition is met on the last prime,
            # then check if (last prime + 2) is prime. If it
            # is not, then check i+6n, i+6n+2, for n -> inf
            #
            # If the first condition is not met, then the second
            # condition will, so jump 4 (to complete a cycle) to
            # check the next prime, and repeat i+6n, i+6n+2
            prime = self.buffer[-1]
            if (prime - 5) % 6 == 0:
                prime += 2
                if self._fastcontains(prime):
                    self.buffer.append(prime)
                    return prime

            prime += 4
            while True:
                if self._fastcontains(prime):
                    self.buffer.append(prime)
                    return prime
                prime += 2

                if self._fastcontains(prime):
                    self.buffer.append(prime)
                    return prime
                prime += 4
        else:
            return self.buffer[self.i]

    @staticmethod
    def _canbeprime(n):
        # Assume odd number ≥ 5
        return ((n - 5) % 6 == 0) or ((n - 7) % 6 == 0)

    def _fastcontains(self, n):
        # This won't handle special cases (< 5) neither perform check
        # whether it can possibly be prime or not (_canbeprime)
        limit = int(n**0.5)
        for p in self.buffer:
            if p > limit:
                return True
            if n % p == 0:
                return False

        raise ValueError('The gap between primes was incredibly large. This should not ever happen.')

    def __contains__(self, n):
        # Special cases
        if n < 2:
            return False
        if n < 4:
            return True

        # Fast check
        if not self._canbeprime(n):
            return False

        # Check prime factors
        limit = int(n**0.5)
        for p in self.buffer:
            if p > limit:
                return True
            if n % p == 0:
                return False

        # "Slow" fallback, never called when invoked sequentially (via iterator)
        for i in range(self.buffer[-1]+2, limit + 1, 2):
            if n % i == 0:
                return False

        return True


class primeseq(infprimeseq):
    def __init__(self, stop, initial_buffer_size=None):
        super().__init__(initial_buffer_size=initial_buffer_size)
        self.stop = stop

        # After everything has been initialized, we can now override __next__
        def nxt(slf):
            p = super().__next__()
            if p < slf.stop:
                return p
            else:
                raise StopIteration()

        self.__next__ = nxt


if __name__ == '__main__':
    print('Testing…')
    ps = infprimeseq()
    for i in range(0, 10000):
        if (i in ps) != is_safe_prime(i):
            if is_safe_prime(i):
                print(i, '\tshould     be prime, but is it in ps?:', i in ps)
            else:
                print(i, '\tshould not be prime, but is it in ps?:', i in ps)
    print('Test done.')
