from math import factorial, exp


def perm(n):
  """Permutations.
     n = number of elements

     Notation: P
                n

     All elements included: yes
     Can elements repeat:   no
     Order matters:         yes

     See: Number of ways there are to rearrange n elements.

     Practical example: amount of numbers with 3 distinct digits.
     Let the elements be: 1, 2, 3:

       123, 132, 213, 231, 312, 321
  """
  return factorial(n)


def rperm(n, *ks):
  """Permutations (allowing repetition).
     n = total number of elements
     ks = how many times the first, second, etc, element repeats

                 a,b,c…
     Notation: PR
                 n

     All elements included: yes
     Can elements repeat:   yes
     Order matters:         yes

     See: Number of ways there are to rearrange n elements,
          some of them possibly repeated.

     Practical example: amount of numbers with 3 digits.
     Let the elements be: 1, 1, 2:

       112, 121, 211
  """
  divisor = 1
  for k in ks:
    divisor *= k
  return perm(n) / divisor


def vari(n, k):
  """Variations.
     n = total number of elements
     k = number of elements chosen

                k
     Notation: V
                n

     All elements included: no
     Can elements repeat:   no
     Order matters:         yes

     See: Number of ways there are to rearrange k elements
          from the set of n elements without repetition.

     Practical example: amount of numbers with 3 digits.
     Let the elements be: 1, 2, 3, 4:

       123, 132, 213, 231, 312, 321,
       124, 142, 214, 241, 412, 421
  """
  # n! / (n-k)!
  result = 1
  for i in range(n-k+1, n+1):
    result *= i
  return result


def rvari(n, k):
  """Variations (allowing repetition).
     n = total number of elements
     k = number of elements chosen

                 k
     Notation: VR
                 n

     All elements included: no
     Can elements repeat:   yes
     Order matters:         yes

     See: Number of ways there are to rearrange k elements
          from the set of n elements, being able to choose
          some element more than once.

     Practical example: amount of numbers with 2 digits.
     Let the elements be: 1, 2, 3:

       11, 22, 33, 12, 21, 13, 31, 23, 32
  """
  return n ** k


def combs(n, k):
    """Combinations.
       n = total number of elements
       k = number of elements chosen

                  k                          ⎛n⎞
       Notation: C        or "n choose k" as ⎝k⎠
                  n

       All elements included: no
       Can elements repeat:   no
       Order matters:         no

       See: Number of sets with k elements from the original set of n.

       Practical example: 2 winners are chosen from a group of 4.
       Let the people be called: A, B, C, D

         AB, AC, AD, BC, BD, CD

       Some properties of the combinatory numbers are:

         ⎛n⎞   ⎛n⎞
         ⎝0⎠ = ⎝n⎠ = 1

         ⎛n⎞   ⎛ n ⎞
         ⎝k⎠ = ⎝n-k⎠

         ⎛ n ⎞   ⎛n⎞   ⎛n+1⎞
         ⎝k-1⎠ + ⎝k⎠ = ⎝ k ⎠
    """
    # n! / k!(n-k)!
    return vari(n, k) / perm(k)


def rcombs(n, k):
    """Combinations (allowing repetition)
       n = total number of elements
       k = number of elements chosen

       Number of possible groups with k elements from n elements,
       and the order doesn't matter.

                 k           ⎛n+k-1⎞
     Notation: CR        or  ⎝  k  ⎠
                 n

     All elements included: no
     Can elements repeat:   yes
     Order matters:         no

     See: Number of sets with k elements from the original set of n,
          where any element can be chosen more than once

     Practical example: 2 souvenirs must be chosen from 4 available
     Let the souvenirs be called: A, B, C, D

       AA, AB, AC, AD, BB, BC, BD, CC, CD, DD
    """
    return combs(n+k-1, k)


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
  g.__dict__['expected'] = 1 / p
  g.__dict__['variance'] = (1-p) / (p**2)
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
  p.__dict__['expected'] = lmbda
  p.__dict__['variance'] = lmbda
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


def pascal(n, left_align=False, extra_line=None):
  """Represents Pascal's triangle with n rows.

     If 'left_align', then the triangle will be left algined.

     If 'extra_line' is None, it will be true if n > 15 for clarity
                     is True, an extra line will always be added
                     is False, no extra line will be added
  """
  rows = [[1]]
  for i in range(n-1):
    row = [1]
    for j in range(i):
      row.append(rows[i][j] + rows[i][j+1])
    row.append(1)
    rows.append(row)
  
  shown = []
  if left_align:
    paddings = tuple(len(str(e)) for e in rows[-1])
    for row in rows:
      show = []
      for i in range(len(row)):
        show.append(str(row[i]).rjust(paddings[i]))
      shown.append(', '.join(show))
  
  else:
    longest = rows[-1][len(rows[-1])//2]
    padding = len(str(longest))
    last = ' '.join(str(e).center(padding) for e in rows[-1])
    for i in range(len(rows)-1):
      show = ' '.join(str(e).center(padding) for e in rows[i])
      shown.append(show.center(len(last)))
    shown.append(last)
  
  if extra_line is None and n > 10:
    extra_line = True
  
  end = '\n\n' if extra_line else '\n'
  print(end.join(s for s in shown))
