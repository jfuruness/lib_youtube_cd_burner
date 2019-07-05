from setuptools import setup, find_packages

setup(
    name='lib_youtube_cd_burner',
    packages=find_packages(),
    version='0.1.00',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_youtube_cd_burner.git',
    download_url='https://github.com/jfuruness/lib_youtube_cd_burner.git',
    keywords=['Furuness', 'furuness', 'pypi', 'package'],  # arbitrary keywords
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[
        'setuptools',
        'psycopg2',
        'requests',
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'burn_a_cd = lib_youtube_cd_burner.__main__:main'
        ]},
)

