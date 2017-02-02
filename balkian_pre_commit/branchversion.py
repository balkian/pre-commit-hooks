import argparse
import semver
import os
from subprocess import check_output

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode()
    error = 1
    for fn in args.filenames:
        with open(fn) as f:
            currentcontent = f.read().strip()
            prevcontent = check_output(['git', 'show', 'HEAD:{}'.format(fn)]).strip().decode()
            current = semver.parse_version_info(currentcontent)
            print('Checking versions: {} -> {}'.format(prevcontent, currentcontent))
            if (branch_name == 'master' and current.prerelease) or\
                (semver.compare(currentcontent, prevcontent)<1):
                return 1
            else:
                error = 0
    return error

if __name__ == '__main__':
    exit(main())
