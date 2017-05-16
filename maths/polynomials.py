from itertools import groupby


# If you have problems with 'rufv' show=True,
# enable the console compatbility mode to use
# more common characters.
compat = False
if compat:
    vbar = '|'
    hbar = '-'
    intersection = '+'
else:
    vbar = '│'
    hbar = '─'
    intersection = '┼'


def ruf(pol, x):
    """For the polynomial 'pol' (a list of its coefficients),
       and a value to test with 'x', returns True if 'x' is
       a root for the polynomial, using the Ruffini's rule.
    """
    c = pol[0]
    for i in range(1, len(pol)):
        c = pol[i] + c*x
    return c == 0


def rufv(pol, x, show=False, show_top=True):
    """Same as 'ruf', but verbose. Returns the factorized
       polynomial iff 'x' is a root for the polynomial.
       
       If 'show' and not 'skip_top', the first line won't be
       shown (useful to chain multiple calls to this method).
    """
    r = [pol[0]]
    for i in range(1, len(pol)):
        r.append(pol[i] + r[-1] * x)
    
    if show:
        #  |pol pol pol
        # x|    r*x r*x
        # -------------
        #  | r   r   r
        lines = ['' for _ in range(4)]
        lines[1] += str(x)
        lines[0] += ' ' * len(lines[1]) + vbar
        lines[2] += hbar * len(lines[1]) + intersection
        lines[1] += vbar
        lines[3]  = lines[0]
        
        for i in range(len(pol)):
            pi  = str(pol[i])
            rx = str(r[i-1] * x) if i != 0 else ''
            ri  = str(r[i])
            pad = max(len(pi), len(rx), len(ri))
            lines[0] += pi.rjust(pad) + ' '
            lines[1] += rx.rjust(pad) + ' '
            lines[3] += ri.rjust(pad) + ' '
            lines[2] += hbar * (pad + 1)
        
        if show_top:
            print('\n'.join(lines))
        else:
            print('\n'.join(lines[1:]))
    
    if r[-1] == 0:
        return r


def findruf(pol, limit=100, show=False):
    """Finds a possible integer root for the given polynomial
       and returns which root this should be. Returns None if
       no root is found within [-limit, limit].

       If 'limit' is None, then the algorithm will never stop.
    """
    # If there is no constant term, then we can divide everything
    # by 'x' to get one grade less, thus, 0 is valid for Ruffini.
    if pol[-1] == 0:
        if show:
            rufv(pol, 0, show=True)
        return 0
    
    if limit is None:
        limit = -1
    
    i = 0
    while i != limit:
        i += 1
        if ruf(pol, i):
            if show:
                rufv(pol, i, show=True)
            return i
        
        if ruf(pol, -i):
            if show:
                rufv(pol, -i, show=True)
            return -i


def intfactorize(pol, limit=100, show=False):
    """Tries to factorize the given polynomial using Ruffini's rule,
       and returns a list of lists containing the coefficients for
       each x's grade (in decreasing, e.g., [2, 4, 1] for 2x² + x⁴ + 1)
    """
    result = []
    show_top = True
    while True:
        r = findruf(pol, limit)
        if r is None:
            break
        
        # Resulting polynomial, without the trailing 0
        pol = rufv(pol, r, show=show, show_top=show_top)[:-1]
        
        # Factor is (x - r)
        result.append([1, -r])
        
        # We're done if the polynomial is grade 2 or less
        if len(pol) <= 2:
            break
        
        # Not showing the top next time
        show_top = False
    
    result.append(pol)
    if show:
        line = []
        for p, items in groupby(sorted(result)):
            line.append('(')
            line.append(strpol(p))
            line.append(')')
            
            count = sum(1 for _ in items)
            if count != 1:
                line.append(strpower(count))
        
        print(''.join(line))
    
    return result


def strpower(i):
    """Stringifies the i'th power"""
    powers = '⁰¹²³⁴⁵⁶⁷⁸⁹'
    if i < 10:
        return powers[i]
    
    result = []
    while i >= 10:
        result.append(powers[i % 10])
        i //= 10
    
    result.append(powers[i])
    return ''.join(reversed(result))


def strpol(pol, add_spaces=True):
    """Stringifies the given polynomial"""
    result = []
    i = len(pol)
    for v in pol:
        i -= 1
        if v == 0:
            continue
        
        if v != 1:
            if v > 1:
                result.append('+')
            result.append(str(v))
        else:
            result.append('+')
        
        if i > 0:
            result.append('x')
            if i > 1:
                result.append(strpower(i))
    
    if result[0] == '+':
        result = ''.join(result[1:])
    else:
        result = ''.join(result)
    
    if add_spaces:
        result = result.replace('+', ' + ').replace('-', ' - ')
    
    return result


if __name__ == '__main__':
    pol = (1, 4, 6, 1, -24, 2)
    print('Stringifying', pol, 'as', strpol(pol))

    pol = (1, 3, 7, 21)
    print('Found root', findruf(pol), 'for', strpol(pol))
    print('About to factorize', strpol(pol), 'as follows:')
    intfactorize(pol, show=True)
    
    pol = (1, -5, 9, -7, 2)
    print('About to factorize', strpol(pol), 'as follows:')
    intfactorize(pol, show=True)
