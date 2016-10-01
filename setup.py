#!/usr/bin/env python
from setuptools import setup


appname = 'sentry_46elks'
appname_slug = appname.replace('_', '-')
version = __import__(appname).__version__

setup(
    name=appname_slug,
    version=version,
    description="Sentry plugin for notifying users by text through the "
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
    entry_points={
        'sentry.plugins': [
            '46elks = {0}.plugin:Sentry46ElksPlugin'.format(appname),
        ],
        'sentry.apps': ['46elks = {0}'.format(appname)],
    },
    install_requires=['requests>=1.0'],
)
