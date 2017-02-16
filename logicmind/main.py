from token_parser import TokenParser
import argparse


def repr_solution(solution, multiline=False):
    names = list(solution.keys())
    names.sort()
    if multiline:
        return '\n'.join('* {}: {}'.format(n, solution[n]) for n in names)
    else:
        return ', '.join('{}: {}'.format(n, '1' if solution[n] else '0') for n in names)


def main():
    parser = argparse.ArgumentParser(description='Logic formulas solution tester.')
    parser.add_argument('formula', metavar='FORMULA', type=str,
                        help='the formula to be tested (e.g. "A <-> [B -> (¬ A)]")')
    parser.add_argument('-s', '--solutions', action='store_true',
                        help='find all the solutions for the given formula')
    parser.add_argument('-t', '--test', type=str,
                        help='the input values to be tested, comma separated, '
                             'value separated by either "=" or ":" (e.g. "A: 1, B: 0")')

    args = parser.parse_args()

    expression = TokenParser.parse_expression(args.formula)
    print('Parsed expression:', repr(expression))

    if args.solutions:
        solutions = expression.find_solutions()
        if solutions:
            if len(solutions) > 1:
                print('Found {} solutions:\n{}'.format(
                    len(solutions),
                    '\n'.join(repr_solution(s) for s in solutions)))
            else:
                print('Found a single solution:\n{}'.format(repr_solution(solutions[0], multiline=True)))
        else:
            print('No solutions were found for the given formula')

        # Leave a new empty line if required
        if args.test:
            print()

    if args.test:
        # Replace ':' by '=' and ';' by ',' to only use '=' and ','
        # Then, split by ',' to get a list of all the values (e.g. 'A = 1')
        solution = args.test\
            .replace(':', '=')\
            .replace(';', ',').split(',')

        # Now split on every '=' to get a pair of values (e.g. 'A', '1')
        solution = [s.split('=') for s in solution]

        # Now create the solution dictionary
        solution = {
            s[0].strip(): s[1].strip() in 'tTyY1' for s in solution
        }

        if expression.apply(solution):
            print(repr_solution(solution), 'is a solution for the given formula.')
        else:
            print(repr_solution(solution), 'is not a solution for the given formula.')
        print()


if __name__ == '__main__':
    main()
