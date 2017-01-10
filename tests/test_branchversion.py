"""
Tests for `branchversion` module.
"""
import pytest
import os
import shutil
import unittest
from contextlib import contextmanager
from subprocess import check_output
from balkian_pre_commit import branchversion 


TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'test-precommit')


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


class TestBalkian_pre_commit(unittest.TestCase):

    def commit_version(self, version, branch='master'):
        with cd(TEMP_DIR):
            check_output(['git', 'checkout', '-B', branch])
            with open('VERSION', 'w') as f:
                f.write(version)
            check_output(['git', 'add', 'VERSION'])
            check_output(['git', 'commit', '-am', 'Committing to branch {}'.format(branch)])

    def initRepo(self):
        self.tearDown()
        os.makedirs(TEMP_DIR)
        check_output(['git', 'init', TEMP_DIR])
        with cd(TEMP_DIR):
            with open('README.md', 'w') as f:
                f.write('Hello')
            check_output(['git', 'add', '.'])
            check_output(['git', 'commit', '-am', 'First commit'])

    def setUp(self):
        self.initRepo()

    def tearDown(self):
        if os.path.isdir(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)

    def test_success(self):
        self.initRepo()
        with cd(TEMP_DIR):
            self.commit_version('0.1.0', 'master')
            assert branchversion.main(['VERSION',])==0

    def test_fail(self):
        self.initRepo()
        with cd(TEMP_DIR):
            self.commit_version('0.1.0-pre.4', 'master')
            assert branchversion.main(['VERSION',])==1
