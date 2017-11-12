"""
Helper script to set up ln -s <desired utilities> on a given bin/ PATH.
"""
import os


utilities = (
    'mineutils/mc',
    'misc/gitmail',
    'misc/pipu',
    'misc/reclick',
)


def run(program, *args):
    """Spawns a the given program as a subprocess and waits for its exit"""
    # I for Invariant argument count, P for using PATH environmental variable
    os.spawnlp(os.P_WAIT, program, program, *args)


if __name__ == '__main__':
    where = None
    try:
        import pyperclip
        where = pyperclip.paste()
        if where.startswith('file://'):
            where = where[len('file://'):]

        if not os.path.isdir(where):
            where = None
    except ImportError:
        pass

    if not where:
        where = input('Where should the links be created?\n: ')

    if not os.path.isdir(where):
        os.makedirs(where)

    utilities = tuple(os.path.abspath(x) for x in utilities)
    os.chdir(where)
    for utility in utilities:
        print(f'Creating link for {utility}...')
        run('ln', '-s', utility)

    print('Done!')
