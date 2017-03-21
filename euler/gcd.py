from primeseq import infprimeseq

primes = infprimeseq()

def get_factors(n):
    """Returns all the prime factors of n"""
    factors = []
    for p in primes:
        c, r = divmod(n, p)
        # While its divisible
        while r == 0:
            # Add this factor
            factors.append(p)
            # Update with the new value after dividing
            n = c
            # And calculate the next division
            c, r = divmod(n, p)
        
        # Once the number is 1, we're done dividing
        if n == 1:
            return factors


def gcd(a, b):
    """Calculates the Greatest Common Divisor using the Euler's algorithm"""
    # a is r₀
    # b is r₁
    # r is r₂
    #
    #         (1)
    # a \_b__     r₀ \_r₁_
    # r   c       r₂   c
    #
    #         (2)
    # b \_r__     r₁ \_r₂_
    # R   c       r₃   c
    r = a % b
    while r != 0:
        a, b, r = b, r, b % r
    return b


def euler_phi(n):
    """Calculates the Euler's Phi function, also known as the
       totient function, by using the prime factors of n"""
    result = n
    for p in set(get_factors(n)):
        result *= (1 - (1 / p))
    return int(result)


def euler_phi_definition(n):
    """Calculates the Euler's Phi function using its definition.
       Chances are this is slower than the method above."""
    result = 1
    for i in range(2, n):
        if gcd(n, i) == 1:
            result += 1
    return result


if __name__ == '__main__':
    for i in range(1, 1000):
        if euler_phi(i) != euler_phi_definition(i):
            print('Found invalid value for i =', i, 'because calculated', euler_phi(i), 'and', euler_phi_definition(i))
            pass
