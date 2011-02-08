#!/usr/bin/env python

from setuptools import setup

setup(
    name = "TracDjangoAuth",
    version = "0.1.2",
    author = "Ville Korhonen",
    author_email = "ville@xd.fi",
    url = "https://github.com/ypcs/TracDjangoAuth",
    download_url = "https://github.com/ypcs/TracDjangoAuth/tarball/master"
    description = "Trac Authentication against Django's userdb",
    
    keywords = [
        'AccountManager',
        'acct_mgr',
        'authentication',
        'Django',
        'Trac',
    ],
    
    packages = [
        'tracdjangoauth',
    ],
    
    install_requires = [
        'Trac>=0.11',
        'TracAccountManager>=0.2',
        'Django>=1.0',
    ],

    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Framework :: Django",
        "Framework :: Trac",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
    ],
    
    entry_points = {
        'trac.plugins': [
            'tracext.auth.django = tracdjangoauth.auth_django',
        ]
    },
)