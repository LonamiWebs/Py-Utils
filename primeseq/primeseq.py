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
    def __init__(self):
        self.buffer = [2, 3, 5]

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1
        if self.i >= len(self.buffer):
            i = self.buffer[-1]+2
            while i not in self:
                i += 2
            self.buffer.append(i)
        return self.buffer[self.i]

    @staticmethod
    def _canbeprime(n):
        # Assume odd number >= 5
        return ((n - 5) % 6 == 0) or ((n - 7) % 6 == 0)

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
        # "Slow" fallback
        for i in range(self.buffer[-1]+2, limit + 1, 2):
            if n % i == 0:
                return False

        return True


class primeseq(infprimeseq):
    def __init__(self, stop):
        super().__init__()
        self.stop = stop

    def __next__(self):
        p = super().__next__()
        if p < self.stop:
            return p
        else:
            raise StopIteration()


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
