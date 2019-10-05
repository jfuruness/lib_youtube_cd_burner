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
    version="0.1.4",
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
        'setuptools>=40.8.0'
        'youtube_dl>=2019.1.17'
        'Flask>=1.1.1'
        'numpy'
        'WTForms>=2.2.1'
        'Flask_WTF>=0.14.2'
        'pydub>=0.23.1'
        'soundfile>=0.10.2'
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
