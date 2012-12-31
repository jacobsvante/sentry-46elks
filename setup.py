#!/usr/bin/env python
from distutils.core import setup
import os
import sys


appname = 'sentry_46elks'
appname_slug = appname.replace('_', '-')
version = __import__(appname).__version__


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print "You probably want to also tag the version now:"
    print "  git tag -a %s -m 'version %s'" % (version, version)
    print "  git push --tags"
    sys.exit()

setup(
    name=appname_slug,
    version=version,
    description="Sentry plugin for notifying users by text through the " \
                "46elks API",
    long_description=open('README.md').read(),
    author='Jacob Magnusson',
    author_email='m@jacobian.se',
    url='https://github.com/jmagnusson/{0}'.format(appname_slug),
    license='New BSD License',
    platforms=['any'],
    packages=[appname],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    entry_points = {
        'sentry.plugins': [
            '46elks = {0}.plugin:Sentry46ElksPlugin'.format(appname),
        ],
        'sentry.apps': ['46elks = {0}'.format(appname)],
    },
    requires = ['requests (>=1.0)'],
)
