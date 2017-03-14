#!/usr/bin/python3.6


def is_constant(s):
    """Determines whether the sequence 's' is constant,
       effectively returning 'true' if 's[i] == s[0]'"""
    return all([s[0] == s[i] for i in range(1, len(s))])


def get_subseq(s, op):
    """Returns the subsequent sequence of applying (op) on the
       sequence 's', in such a way that 'new[i] = old[i+1] (op) old[i]'.
       For example:
        op = lambda a, b: b - a
           → then a difference sequence is returned:
             new[i] = old[i+1] - old[i]
        
        op = lambda a, b: b / a
           → then a division sequence is returned:
             new[i] = old[i+1] / old[i]
        """
    return [op(s[i-1], s[i]) for i in range(1, len(s))]


def get_subseqs(s, op):
    """Returns a list of sequences given when applying (op)
       on them, until a constant one is found, thus:
       new[0] = next seq of s with op
       new[i] = next seq of new[i-1] with op"""
    if len(s) < 2:
        # We can't get the next sequence based on two terms if there's only one
        return []
    
    # Start with the initial subsequence
    subseqs = [get_subseq(s, op)]
    
    # And base the next subsequences on the previous one until they're constant
    while not is_constant(subseqs[-1]) and len(subseqs[-1]) > 1:
        subseqs.append(get_subseq(subseqs[-1], op))
    
    return subseqs


def printtree(s, ss):
    """Prints the table tree for the sequence 's' and its subsequences 'ss'"""
    # Find the term with maximum string length, to use as padding
    pad = max(
              max([len(str(n)) for n in s]),
              max([len(str(n)) for t in ss for n in t]))
    
    # Print the original sequence
    print(' '.join([str(n).center(pad) for n in s]))
    
    # Now print the subsequences
    for i in range(len(ss)):
        # Left pad is shifted by i elements (pad * i)
        # We are centering on the centre (round(pad/2))
        # Minus i to get rid of the extra spaces ' '.join
        leftpad = pad * i + round(pad/2) - i
        print(' ' * leftpad, end='')
        print(' '.join([str(n).center(pad) for n in ss[i]]))


def nextitem(s, op, invop):
    """Tries to guess the next item on the sequence 's' by using a table
       of (op). This method will fail if the sequence doesn't provide enough
       information, and will assume that the latest sequence should remain
       constant.
       
       The inverse operation 'invop' is also required to transverse back
       the tree in order to get the proper results"""
    ds = get_subseqs(s, op)
    # We assume the last item all below Repeats
    r = ds[-1][-1]
    
    # We need to chain this result to the previous ones
    for i in range(len(ds)-2, -1, -1):
        r = invop(ds[i][-1], r)
    
    # Now we have the accumulated inverse operation
    return invop(s[-1], r)


if __name__ == '__main__':
    seq = [6, 9, 2, 5]
    # Using a difference table
    diff  = lambda a, b: b - a
    diffi = lambda a, b: b + a
    
    subseq = get_subseqs(seq, diff)
    printtree(seq, subseq)
    
    print(f'\nNext 2 items of {seq}:')
    for i in range(2):
        seq.append(nextitem(seq, diff, diffi))
        subseq = get_subseqs(seq, diff)
        
        printtree(seq, subseq)
        print()
    
    print('-' * 80)
    print()
    
    seq = [1, 2, 8, 64]
    # Using a division table
    div  = lambda a, b: b // a
    divi = lambda a, b: b  * a
    
    subseq = get_subseqs(seq, diff)
    printtree(seq, subseq)
    
    print(f'\nNext 2 items of {seq}:')
    for i in range(2):
        seq.append(nextitem(seq, div, divi))
        subseq = get_subseqs(seq, div)
        
        printtree(seq, subseq)
        print()
