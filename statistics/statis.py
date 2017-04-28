from math import factorial, exp


def perm(n):
  """Permutations
     n = number of elements

     Number of ways there are to rearrange n elements
  """
  return factorial(n)


def rperm(n, *ks):
  """Permutations (allowing repetition)
     n = total number of elements
     ks = how many times the first, second, etc, element repeats

     Number of ways there are to rearrange n elements,
     with some repeated
  """
  divisor = 1
  for k in ks:
    divisor *= k
  return perm(n) / divisor


def vari(n, k):
  """Variation
     n = total number of elements
     k = number of elements chosen

     On n positions, k elements are chosen (order matters).
     For instance, n = 7, k = 3: '__1_32_'
  """
  return factorial(n) / factorial(n-k)


def rvari(n, k):
  """Variation (allowing repetition)
     n = total number of elements
     k = number of elements chosen
 
     On n positions, k elements (possibly repeated) are chosen (order matters).
     For instance, n = 7, k = 3: '_3__31_'
  """
  return n ** k


def combs(n, k):
    """Combinations
       n = total number of elements
       k = number of elements chosen

       Number of possible groups with k elements from n elements,
       and the order doesn't matter.

       Also known as ⎛n⎞
       "n choose k": ⎝k⎠
    """
    return factorial(n) / (factorial(k) * factorial(n-k))


def rcombs(n, k):
    """Combinations (allowing repetition)
       n = total number of elements
       k = number of elements chosen

       Number of possible groups with k elements from n elements,
       and the order doesn't matter.
    """
    return factorial(n+k-1) / (factorial(k) * factorial(n-k))


def dbinom(n, p):
  """Binomial Distribution
     n = number of repetitions
     p = success probability

     Used when a certain experiment is repeated n times
     with a 0 ≤ P ≤ 1 probability to succeed once.

     This doesn't return a value, but rather the specified binomial function
  """
  def b(k):
    """Returns the probability of k successes"""
    if 0 <= k <= n:
        q = 1 - p
        return rperm(n, k) * p**k * q**(n-k)
    else:
        return 0

  # Allow accessing the used 'n' and 'p' values from the function
  b.__dict__['n'] = n
  b.__dict__['p'] = p
  b.__dict__['expected'] = n * p
  b.__dict__['variance'] = (n * p) * (1-p)
  return b


def dgeom(p):
  """Geometric Distribution
     p = success probability

     Used to determine the probability of a success
     appearing at a given time, with a 0 ≤ P ≤ 1
     probability to succeed once.

     This doesn't return a value, but rather the specified geometric function
  """
  def g(k):
    """Returns the probability that the first success is the k'th success"""
    if 0 < k:
        q = 1 - p
        return q**(k-1) * p
    else:
        return 0

  # Allow accessing the used 'p' value from the function
  g.__dict__['p'] = p
  b.__dict__['expected'] = 1 / p
  b.__dict__['variance'] = (1-p) / (p**2)
  return g


def dpois(lmbda):
  """Poisson Distribution
     lmbda = average number of successes per unit interval

     Used to determine the probability of an amount of
     successes occuring in a fixed interval (time, area…)

     This doesn't return a value, but rather the specified Poisson function
  """
  def p(k):
    if 0 <= k:
      return (exp(-lmbda) * lmbda**k) / factorial(k)
    else:
      return 0

  # Allow accessing the used 'lmbda' value from the function
  p.__dict__['lmbda'] = lmbda
  b.__dict__['expected'] = lmbda
  b.__dict__['variance'] = lmbda
  return p


def hist(f, n, height=20, c='│'):
  """Represents a Historiogram
     f = function to represent
     n = number of elements to represent = [0, 1, …, n-1, n]
     height = maximum height to show in rows
     c = character to use for the representation
  """
  # Calculate the images
  ys = [f(x) for x in range(n+1)]
  ymax = max(ys)

  # Define n steps evenly dividing the height
  # by considering ymax to be as tall as height
  step_size = ymax / height
  steps = [step_size * i for i in range(height)]

  # Always append the highest value so its represented
  steps.append(ymax)

  # We print to the console from above
  for s in reversed(steps):
    print('%04.1f' % (100 * s), end='% ')

    # For each value, we check if its the current step
    # is below its probability, then it should be filled
    for y in ys:
      print(c if s <= y else ' ', end=' ')
    print()

