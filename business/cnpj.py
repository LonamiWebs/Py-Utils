"""
This module provides a wrapper class to use with
CNPJ (CGC), which in addition to offering a simple verification method,
with methods for comparison and conversion.


>>> a = CNPJ('11222333000181')
>>> b = CNPJ('11.222.333/0001-81')
>>> c = CNPJ([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])
>>> assert a.isValid()
>>> assert b.isValid()
>>> assert not c.isValid()
>>> assert a == b
>>> assert not b == c
>>> assert not a == c
>>> assert eval(repr(a)) == a
>>> assert eval(repr(b)) == b
>>> assert eval(repr(c)) == c
>>> assert str(a) == \"11.222.333/0001-81\"
>>> assert str(b) == str(a)
>>> assert str(c) == \"11.222.333/0001-82\"
"""


class CNPJ(object):

    def __init__(self, cnpj):
        """Class representing a number of CNPJ

        >>> a = CNPJ('11222333000181')
        >>> b = CNPJ('11.222.333/0001-81')
        >>> c = CNPJ([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])

        """
        try:
            basestring
        except:
            basestring = (str, unicode)

        if isinstance(cnpj, basestring):
            if not cnpj.isdigit():
                cnpj = cnpj.replace(".", "")
                cnpj = cnpj.replace("-", "")
                cnpj = cnpj.replace("/", "")

            if not cnpj.isdigit:
                raise ValueError("Value does not follow the form xx.xxx.xxx/xxxx-xx")

        if len(cnpj) < 14:
            raise ValueError("The CNPJ number must be 14 digits")

        self.cnpj = map(int, cnpj)


    def __getitem__(self, index):
        """Returns the digit in index as string

        >>> a = CNPJ('11222333000181')
        >>> a[9] == '0'
        True
        >>> a[10] == '0'
        True
        >>> a[9] == 0
        False
        >>> a[10] == 0
        False

        """
        return str(self.cnpj[index])

    def __repr__(self):
        """Returns a 'real' representation, that is:

        eval(repr(cnpj)) == cnpj

        >>> a = CNPJ('11222333000181')
        >>> print repr(a)
        CNPJ('11222333000181')
        >>> eval(repr(a)) == a
        True

        """
        return "CNPJ('%s')" % ''.join([str(x) for x in self.cnpj])

    def __eq__(self, other):
        """Provides equality test for CNPJ numbers

        >>> a = CNPJ('11222333000181')
        >>> b = CNPJ('11.222.333/0001-81')
        >>> c = CNPJ([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])
        >>> a == b
        True
        >>> a != c
        True
        >>> b != c
        True

        """
        if isinstance(other, CNPJ):
            return self.cnpj == other.cnpj
        return False

    def __str__(self):
        """Returns a CNPJ string in dashed and dashed form

        >>> a = CNPJ('11222333000181')
        >>> str(a)
        '11.222.333/0001-81'

        """
        d = ((2, "."), (6, "."), (10, "/"), (15, "-"))
        s = map(str, self.cnpj)
        for i, v in d:
            s.insert(i, v)
        r = ''.join(s)
        return r

    def isValid(self):
        """Valid the cnpj number

        >>> a = CNPJ('11.222.333/0001-81')
        >>> a.isValid()
        True
        >>> b = CNPJ('11222333000182')
        >>> b.isValid()
        False

        """
        cnpj = self.cnpj[:12]
        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        # we took only the first 9 digits of the CNPJ and generated the remaining two digits
        while len(cnpj) < 14:

            r = sum([x*y for (x, y) in zip(cnpj, prod)])%11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            cnpj.append(f)
            prod.insert(0, 6)

        # if the number with the missing digits matches the original number, then it is valid
        return bool(cnpj == self.cnpj)

if __name__ == "__main__":
    import doctest, sys
    doctest.testmod(sys.modules[__name__])