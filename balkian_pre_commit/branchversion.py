import argparse
import semver
from subprocess import check_output


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    gitout = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    branch_name = gitout.strip().decode()

    if len(args.filenames) > 1:
        print('There are more than one VERSION files: '
              '{}'.format(args.filenames))
        return 1
    elif not args.filenames:
        if branch_name == 'master':
            print('VERSION files should be bumped in every commit to master')
            return 2
        else:
            return 0

    fn = args.filenames[0]
    with open(fn) as f:
        currentcontent = f.read().strip()
        gitout = check_output(['git', 'show', 'HEAD:{}'.format(fn)])
        prevcontent = gitout.strip().decode()
        current = semver.parse_version_info(currentcontent)
        print('Checking versions: {} -> {}'.format(prevcontent,
                                                   currentcontent))
        if branch_name == 'master' and current.prerelease:
            print('Trying to push a pre-release version to a master branch')
            return 1
        elif semver.compare(currentcontent, prevcontent) < 1:
            print('The new version should be newer than the old one')
            return 1
        else:
            return 0


if __name__ == '__main__':
    exit(main())
