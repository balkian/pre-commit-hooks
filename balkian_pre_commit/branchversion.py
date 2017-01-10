import argparse
import semver
import os
from subprocess import check_output

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode()
    if branch_name == 'master':
        for fn in args.filenames:
            if os.path.basename(fn) == 'VERSION':
                with open(fn) as f:
                    version = semver.parse_version_info(f.read())
                    if version.prerelease:
                        return 1
    return 0
            
if __name__ == '__main__':
    exit(main())
