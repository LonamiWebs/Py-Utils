#!/usr/bin/python3

from adb import *
import os

print('Loading packages...')
packages = [pp[1] for pp in enumerate_packages()]


def interactive_search_package():
    while True:
        query = input('Please enter the package name (or a part of it): ')
        if not query:
            return None

        for pkg in [p for p in packages if query in p.lower()]:
            if input('Is "{}" the package you want (y/n)?: '.format(pkg)) == 'y':
                return pkg

        print('There are no more packages matching your query.')


def interactive_search_packages():
    found = []
    while True:
        print()
        if found:
            print('Currently added packages:')
            for pkg in found:
                print(' -', pkg)
        else:
            print('There are no packages added yet.')

        print('Enter another string to look for packages to add (empty to exit)')
        pkg = interactive_search_package()
        if pkg:
            found.append(pkg)
        else:
            break

    return found


def option_backup_packages():
    to_backup = interactive_search_packages()

    include_apk = input('Include .apk (Y/n)?: ') != 'n'
    include_obb = input('Include .obb (Y/n)?: ') != 'y'
    include_shared = input('Include shared (internal storage files) (y/N)?: ') == 'y'

    print('Performing backup...')
    output = backup_packages(to_backup, apk=include_apk, obb=include_obb, shared=include_shared)
    print('Backup file created at {}.'.format(output))


def get_info(backup_file):
    match = re.match('(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})-(\d)packages.ab', backup_file)
    if match:
        return datetime(year=int(match.group(1)),
                        month=int(match.group(2)),
                        day=int(match.group(3)),
                        hour=int(match.group(4)),
                        minute=int(match.group(5))), int(match.group(6))

    return None, None


def option_restore_packages():
    backups = [f for f in os.listdir('.') if f.endswith('.ab')]
    if not backups:
        print('There are no backups available.')
        return

    print('Available backups:')
    for i, backup in enumerate(backups):
        date, count = get_info(backup)
        if not date:
            print(' {}. {} (Unknown backup)'.format(i, backup))
        else:
            print(' {}. {} packages, made the {}'.format(i, count, date))

    idx = int(input('Which backup do you want to restore?: '))
    backup = backups[idx]
    print('Restoring backup file {}...'.format(backup))
    restore_backup(backup)
    print('Backup restored.')


if __name__ == '__main__':
    print('Available options:')
    print(' 1. Backup packages')
    print(' 2. Restore backups')
    option = input('What do you wanna do?: ')
    if option == '1':
        option_backup_packages()
    elif option == '2':
        option_restore_packages()
