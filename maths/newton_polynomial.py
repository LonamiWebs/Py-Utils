#!/usr/bin/python3.6


import unittest


"""
Spanish preface
===============

Dada la secuencia: `6, 9, 2, 5, …`
- Definimos `f₀(x_i)`: Término i-ésimo de la secuencia.
- Definimos `p₀(x)`: Término primero de la secuencia x₀, ya que este es el
                     único valor que satisface la secuencia (al principio).
                     Es obvio, ya que el primer término = primer término.

La pendiente de la recta de grado 1 que interpola entre x₀, x₁ es:
f₁(x₀, x₁) = [f(x₁) - f(x₀)] / (x₁ - x₀)
           = [f(x₁) - f(x₀)]

Esto nos da la pendiente para pasar de f(x₀) a f(x₁), que efectivamente,
es sumar una unidad de la pendiente (1 * pendiente).

Esto asumiendo que los términos de la secuencia son `x₀ = 0, x₁ = 1, …`,
nos permite eliminar la parte de ` / (x₁ - x₀)`.

Es decir, los términos equivalen a su posición, por lo tanto la distancia
entre dos valores consecutivos es siempre la unidad.

--

Para construir el polinomio y preservar la información que ya tenemos (nuestro
polinomio ya sabe el primer término de la secuencia), multiplicamos la pendiente
actual por `x`. Así, en el primer paso x₀, este término se anula preservando p₀.

Nótese, si hubieramos elegido `x₀ = 1, x₁ = 2, x₂ = 3, …` para los valores de
la secuencia, entonces deberíamos multiplicar por `x-1` en el primer paso x₀,
para que para el valor 1 se anulase con el x₀ = 1.

En nuestro caso, el primer término al ser 0, usamos `x` a secas (= x - 0).

--

En resumen:
                             v para preservar el primer valor x₀
p₁(x) = p₀(x) + f(x₀,  x₁) * x
      = p₀(x) + pendiente1 * x
grado 0 ^ (cte)      grado 1 ^

--

Para construir el polinomio de grado 2 y preservar el anterior, de nuevo,
multiplicaremos por `x` y por `x-1`. Así, en los pasos x₀ y x₁, la información
anterior se preserva, porque el nuevo término se anula.

La nueva pendiente de grado 2 se calcula como:
f₂(x₀, x₁, x₂) = [f₁(x₁, x₂) - f₁(x₀, x₁)] / (x₂ - x₀)
               = [f₁(x₁, x₂) - f₁(x₀, x₁)] / 2

Nuevamente, podemos simplificar `x₂-x₀ = 2` porque hemos asumido que cada
término i-ésimo equivale a su posición. Esto es válido además para cualquier
pareja (e.g., x₅ y x₇).

Es de nuevo la diferencia entre un paso `f(x₀, x₁)` y el siguiente `f(x₁, x₂)`.
Se puede obserbar como los pasos son desde (inicio,   final-1) y el siguiente,
todo desplazado en una unidad es decir así (inicio+1, final-1+1)

--

Con esto construimos el polinomio:
p₂(x) = p₁(x) + f₂(x₀, x₁, x₂) * x * (x-1)
        p₁(x) +  pendiente 2ª  * x * (x-1)


Ya se puede intuir una generalización:
p_i(x) = p_i-1(x) + f_i(x₀, …, x_i) * x * (x-1) * … * (x-(i-1))
"""


def f(s, e):
    """Returns the slope function for the given (start, end) indices f(x_s, x_e)
       For example, `f(x₀, x₁, x₂) = f(0, 2)` (starts at 0, ends at 2)"""
    if s > e:
        raise ValueError('The starting index `s` must be ≤ index `e`')
    
    if s == e:
        # End and start are the same, so it's the single i'th = s = e value.
        # The x_i terms are given from the sequence, so the i'th term is seq[i].
        def base(seq):
            """Base case f₀ (slope function)"""
            # We don't actually care about a real x value here, since
            # we only want to use the i'th term of the sequence (s = e).
            #
            # Why don't we care about the `x` here? This is f₀, then x⁰ = 1.
            # This means that the slope with no degree is constant.
            if s >= len(seq):
                raise ValueError(f'Cannot retrieve the slope of degree {s} '+
                                  'on a sequence with only {len(seq)} items')
            
            return seq[s]
        
        return base
    else:
        def nonbase(seq):
            """Non-base case f_i (slope function).
               Assuming x to be the start index"""            
            # Imagine start and end are 0 and 1 respectively
            # We are left with a degree = (end - start) = 1
            #
            # Now that we know the grade, we can define the slope function:
            # f_degree = f_degree-1(end) - f_degree-1(start)
            #
            # For the case where the grade is 1:
            # f₁ = f₀(e) - f₀(s)
            #
            # For the case where the grade is 2:
            # f₂ = f₁(e) - f₁(s)
            #
            # And so on, each of which invoke the previous degree version.
            #
            # To get the previous starting slope function, with one degree
            # less, we simply reduce the end by one unit so we get the previous
            # function which still starts at the start `s`.
            f_s = f(s, e-1)
            
            # And to get the next step, we simply add one on both sides,
            # so we get (start+1, end-1+1) which is (start+1, end):
            f_e = f(s+1, e)
            
            # Now we can calculate the difference between these and divide
            # by their step as we would do with any other case
            return (f_e(seq) - f_s(seq)) / (e - s)
        
        return nonbase


def p(sequence, g=None):
    """Returns the polynomial from the given sequence.
       If no degree g is specified, the degree = `len(sequence)-1` is used"""
    if not sequence:
        raise ValueError('Cannot retrieve the polynomial of an empty sequence')
    
    if g is None:
        g = len(sequence) - 1
    
    # The polynomial p_i was defined is follows:
    # p_i(x) = p_i-1(x)          + f_i(x₀, …, x_i) * (x * (x-1) * … * (x-i+1))
    #          ^ previous degree + ^ slope for i     ^ preserving previous state
    if g == 0:
        # Degree 0 is defined as being the first value from the sequence,
        # so this is the base case p₀.
        #
        # Why is it the first case? Because it satisfies the first term
        # of the sequence when no `x` is actually involved. Once again,
        # we don't need the actual value of the `x` really because it's x⁰ = 1.
        def base(x):
            """Base case p₀ (the first value of the sequence)"""
            return sequence[0]
        
        return base
    else:
        def nonbase(x):
            """Non-base case p_i (polynomial function)"""
            # It's defined as the previous polynomial plus…
            prev_p = p(sequence, g - 1)
            
            # …the slope of this grade (starting on the sequence)…
            f_g = f(0, g)
            slope = f_g(sequence)
            
            # …which is multiplied by `x*(x-1)*…*(x-i+1)` to keep the old state
            for i in range(g):
                # i will go from 0 (x), 1 (x-1), 2 (x-2), …, g-1 (x-(g-1))
                slope *= (x - i)
            
            # And there we have it!
            return prev_p(x) + slope
        
        return nonbase


class InterpolationTests(unittest.TestCase):
    def setUp(self):
        self.sequence = [6.0, 9.0, 2.0, 5.0]
        #                ^    ^    ^    ^
        #                0th  1st  2nd  3rd

    def test_slope_degree_1(self):
        # f(x₀, x₁) = (9-6) / (1-0) =  3.0
        # f(x₁, x₂) = (2-9) / (2-1) = -7.0
        # f(x₂, x₃) = (5-2) / (3-2) =  3.0
        self.assertEqual(f(0, 1)(self.sequence),  3.0)
        self.assertEqual(f(1, 2)(self.sequence), -7.0)
        self.assertEqual(f(2, 3)(self.sequence),  3.0)
    
    def test_polynomial_guess(self):
        # The polynomial should return the same value as the original sequence
        p3 = p(self.sequence)
        for i in range(len(self.sequence)):
            self.assertEqual(p3(i), self.sequence[i])


if __name__ == '__main__':
    unittest.main()
