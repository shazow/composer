#!/usr/bin/env python

from distutils.core import setup

import os
import re


try:
    import setuptools
except ImportError, _:
    pass # No 'develop' command, oh well.

base_path = os.path.dirname(__file__)

# Get the version (borrowed from SQLAlchemy)
fp = open(os.path.join(base_path, 'composer', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(fp.read()).group(1)
fp.close()


version = VERSION

requirements = [
    'werkzeug',
]

tests_requirements = requirements + [
    'nose',
]

setup(name='Composer',
      version=version,
      description="Compose dynamic templates and markup into a static website.",
      long_description=open('README.rst').read() + '\n\n' + open('CHANGES.rst').read(),
      keywords='template compile dynamic static web html mako',
      author='Andrey Petrov',
      author_email='andrey.petrov@shazow.net',
      url='https://github.com/shazow/composer',
      license='MIT',
      packages=['composer'],
      requires=requirements,
      tests_require=tests_requirements,
      entry_points="""
      [console_scripts]
      composer = composer.command:main
      """
      )


print """
---

%s

---

You can install all the optional dependencies with: ::

    pip install -r optional.txt

""" % open('optional.txt').read().strip()
