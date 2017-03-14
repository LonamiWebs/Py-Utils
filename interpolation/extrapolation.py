def getdiff(s):
    """Returns the sequence of the differences on the
       sequence 's', in such a way that 'new[i] = old[i+1] - old[i]'"""
    return [s[i] - s[i-1] for i in range(1, len(s))]


def isconstant(s):
    """Determines whether the sequence 's' is constant,
       effectively returning 'true' if 's[i] == s[0]'"""
    return all([s[0] == s[i] for i in range(1, len(s))])


def getdiffs(s):
    """Returns a list of sequences representing the difference
       of the previous sequences until a constant one is found, thus:
       new[0] = differences s
       new[i] = differences new[i-1]"""
    if len(s) < 2:
        # We can't get the differences between two terms if there's only one
        return []
    
    # Start with the initial difference
    diffs = [getdiff(s)]
    
    # And base the next differences on the previous one until they're constant
    while not isconstant(diffs[-1]) and len(diffs[-1]) > 1:
        diffs.append(getdiff(diffs[-1]))
    
    return diffs


def printtree(s):
    """Prints the difference table tree for the sequence 's'"""
    ds = getdiffs(s)
    # Find the term with maximum string length, to use as padding
    pad = max(
              max([len(str(n)) for n in s]),
              max([len(str(n)) for d in ds for n in d]))
    
    # Print the original sequence
    print(' '.join([str(n).center(pad) for n in s]))
    
    # Now print the differences
    for i in range(len(ds)):
        # Left pad is shifted by i elements (pad * i)
        # We are centering on the centre (round(pad/2))
        # Minus i to get rid of the extra spaces ' '.join
        leftpad = pad * i + round(pad/2) - i
        print(' ' * leftpad, end='')
        print(' '.join([str(n).center(pad) for n in ds[i]]))


def nextitem(s):
    """Tries to guess the next item on the sequence 's' by using a table of
       differences. This method will fail if the sequence doesn't provide
       enough information, and will assume that the latest sequence should
       remain constant"""
    ds = getdiffs(s)
    # We assume the last item all below Repeats
    r = ds[-1][-1]
    
    # We need to chain this result to the previous ones
    for i in range(len(ds)-2, -1, -1):
        r = ds[i][-1] + r
    
    # Now we have the accumulated addition
    return s[-1] + r


if __name__ == '__main__':
    seq = [6, 9, 2, 5]
    printtree(seq)
    print(f'\nNext 2 items of {seq}:')
    for i in range(2):
        seq.append(nextitem(seq))
        printtree(seq)
        print()
