from setuptools import setup, find_packages

setup(
    name='lib_youtube_cd_burner',
    packages=find_packages(),
    version='0.1.00',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_youtube_cd_burner.git',
    download_url='https://github.com/jfuruness/lib_youtube_cd_burner.git',
    keywords=['Furuness', 'cd', 'burner', 'youtube', 'audio', 'audio cd'],
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[
        'setuptools',
        'pydub',
        'soundfile',
        'youtube_dl',
        'setuptools',
        'psycopg2',
        'requests',
        'numpy'
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
            'burn_a_cd = lib_youtube_cd_burner.__main__:main'
        ]},
)

