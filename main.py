from token_parser import TokenParser


def main():
    # Example: A <-> [B -> (¬ A)]
    e = input('Enter expression: ')
    e = TokenParser.parse_expression(e)

    print('I found these solutions…', e.find_solutions())

    solutions = {}
    for v in e.get_variables():
        solutions[v] = input('Value for ' + v + ' (T/F): ') in 'tTyY1'

    print('Expression is', 'true.' if e.apply(solutions) else 'false.')


if __name__ == '__main__':
    main()
