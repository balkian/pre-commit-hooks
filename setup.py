import pip
from setuptools import setup
from pip.req import parse_requirements
# parse_requirements() returns generator of pip.req.InstallRequirement objects

try:
    install_reqs = parse_requirements(
        "requirements.txt", session=pip.download.PipSession())
    test_reqs = parse_requirements(
        "test-requirements.txt", session=pip.download.PipSession())
except AttributeError:
    install_reqs = parse_requirements("requirements.txt")
    test_reqs = parse_requirements("test-requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
install_reqs = [str(ir.req) for ir in install_reqs]
test_reqs = [str(ir.req) for ir in test_reqs]

from balkian_pre_commit import __version__

setup(
    name='balkian_pre_commit',
    packages=['balkian_pre_commit'],  # this must be the same as the name above
    version=__version__,
    description='''pro-commit hooks for various projects''',
    author='J. Fernando Sánchez',
    author_email='balkian@gmail.com',
    # use the URL to the github repo
    url='https://github.com/balkian/balkian-pre-commit',
    download_url=('https://github.com/balkian/balkian-pre-commit/'
                  'archive/{}.tar.gz'.format(__version__)),
    package_dir={'balkian_pre_commit': 'balkian_pre_commit'},
    keywords='pre-commit-hooks',
    install_requires=install_reqs,
    tests_require=test_reqs,
    setup_requires=['pytest-runner', ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'branchversion = balkian_pre_commit.branchversion:main',
        ]
    },
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)
