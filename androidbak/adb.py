from subprocess import check_output
from datetime import datetime
import re


def run_adb_command(command):
    """Runs the given command (arguments) through adb"""
    return str(check_output('./adb {}'.format(command), shell=True), encoding='utf-8')


def enumerate_packages():
    """Enumerates where the .apk files are located and the package name"""
    for line in run_adb_command('shell pm list packages -f').split('\n'):
        match = re.match(r'package:([\w\d/.-]+.apk)=([\w\d.]+)', line)
        if match:
            yield match.group(1), match.group(2)


def backup_packages(packages, apk=True, obb=True, shared=False):
    """Backups the given packages and returns the output file name"""
    args = []
    if apk: args.append('-apk')
    if obb: args.append('-obb')
    if shared: args.append('-shared')
    output = '{}-{}packages.ab'.format(datetime.now().strftime('%Y%m%d-%H%M'),
                                       len(packages))

    run_adb_command('backup -f {} {} {}'.format(output, ' '.join(args), ' '.join(packages)))
    return output


def restore_backup(backup_file):
    """Restores the specified backup file"""
    run_adb_command('restore {}'.format(backup_file))
