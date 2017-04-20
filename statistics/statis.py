from math import factorial


def perm(n):
  """Permutations
     n = number of elements

     Number of ways are to rearrange n elements
  """
  return factorial(n)


def rperm(n, k):
  """Permutations (allowing repetition)
     n = total number of elements
     k = number of elements chosen

     On n positions, k elements are chosen (order doesn't matter).
     For instance, n = 7, k = 3: '_X__XX_'

     Also known as ⎛n⎞
     "n choose k": ⎝k⎠
  """
  return perm(n) / (perm(k) * perm(n-k))


def vari(n, k):
  """Variation
     n = total number of elements
     k = number of elements chosen

     On n positions, k elements are chosen (order matters).
     For instance, n = 7, k = 3: '__1_32_'
  """
  return rperm(n, k) * rperm(k)


def rvari(n, k):
  """Variation (allowing repetition)
     n = total number of elements
     k = number of elements chosen
 
     On n positions, k elements (possibly repeated) are chosen (order matters).
     For instance, n = 7, k = 3: '_3__31_'
  """
  return n ** k


def dbinom(n, p):
  """Binomial Distribution
     n = number of repetitions
     p = success probability

     Used when a certain experiment is repeated n times
     with a 0 ≤ P ≤ 1 probability to succeed.

     This doesn't return a value, but rather the specified binomial function
  """
  def b(k):
    q = 1 - p
    return rperm(n, k) * p**k * q**(n-k)
  b.__dict__['n'] = n
  b.__dict__['p'] = p
  return b


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

  # We print the console from above
  for s in reversed(steps):
    print('%04.1f' % (100 * s), end='% ')

    # For each value, we check if its the current step
    # is below its probability, then it should be filled
    for y in ys:
      print(c if s <= y else ' ', end=' ')
    print()

