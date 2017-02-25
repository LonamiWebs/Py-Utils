# Available spaces inside the menu
available_spaces = 60


# Prints
def print_start():
    print('┌{}┐'.format('─' * available_spaces))


def print_empty():
    print('│{}│'.format(' ' * available_spaces))


def print_left(value, padding=1):
    print('│{}{}│'.format(' ' * padding, value.ljust(available_spaces - padding)))


def print_center(value):
    print('│{}│'.format(value.center(available_spaces)))


def print_right(value, padding=1):
    print('│{}{}│'.format(value.rjust(available_spaces - padding), ' ' * padding))


def print_separator():
    print('├{}┤'.format('─' * available_spaces))


def print_end():
    print('└{}┘'.format('─' * available_spaces))


def print_enter_to_continue():
    print_separator()
    print_left('Press enter to continue.')
    print_end()
    input('⬜️ ')


def print_title(title):
    clear()
    print_start()
    print_center(title)
    print_separator()


def clear():
    print('\n' * 100)
