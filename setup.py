#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module sets up the package for the lib_youtube_cd_burner"""

from setuptools import find_packages, setup

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Production"

setup(
    name="lib_youtube_cd_burner",
    version="0.2.1",
    url="https://github.com/jfuruness/lib_youtube_cd_burner.git",
    download_url='https://github.com/jfuruness/lib_youtube_cd_burner.git',
    keywords=['Furuness', 'cd', 'burner', 'youtube', 'audio', 'audio cd'],
    license="BSD",
    description="Downloads youtube playlists and saves or formats them",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'setuptools',
        'youtube_dl',
        'Flask',
        'mutagen',
        'numpy',
        'WTForms',
        'Flask_WTF',
        'pydub',
        'soundfile'
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'youtube_cd_burner = lib_youtube_cd_burner.__main__:main'
        ]},
)
