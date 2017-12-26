# -*- coding: utf-8 -*-

import re
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class DjangoTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

        test_dir = os.path.dirname(__file__)
        sys.path.insert(0, test_dir)
        import django
        from django.test.utils import get_runner
        from django.conf import settings
        django.setup()

        runner = get_runner(settings)(
            verbosity=1,
            interactive=False, failfast=False
        )
        errno = runner.run_tests(['tests'])
        sys.exit(errno)


here = os.path.dirname(__file__)

with open(os.path.join(here, 'variantmpl', '__init__.py'), 'r') as f:
    version = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

with open(os.path.join(here, 'README.rst')) as fp:
    readme = fp.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    'Django',
]

classifiers = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 1.10',
    'Framework :: Django :: 1.11',
    'Framework :: Django :: 2.0',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]


setup(
    name='django-variantmpl',
    version=version,
    packages=find_packages(exclude=['tests', 'tests.*']),
    license='MIT',
    keywords='django templates switch useragent',
    description='Provide a mechanism for Django that switching template based on request context.',  # NOQA
    long_description=readme,
    url='https://github.com/tell-k/django-variantmpl',
    install_requires=install_requires,
    cmdclass={'test': DjangoTest},
    author='tell-k',
    author_email='ffk2005@gmail.com',
    classifiers=classifiers,
)
