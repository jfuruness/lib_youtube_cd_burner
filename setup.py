from setuptools import setup, find_packages

setup(
    name='lib_youtube_cd_burner',
    packages=find_packages(),
    version='0.1.0',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_youtube_cd_burner.git',
    download_url='https://github.com/jfuruness/lib_youtube_cd_burner.git',
    keywords=['Furuness', 'cd', 'burner', 'youtube', 'audio', 'audio cd'],
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
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
