from m2r import parse_from_file
from setuptools import setup, find_packages

import pytest_pytestrail

setup(
    name='pytest-pytestrail',
    description='pytest plugin for interaction with TestRail',
    long_description=parse_from_file('README.md'),
    version=pytest_pytestrail.__version__,
    author='tolstislon',
    author_email='tolstislon@gmail.com',
    url='https://github.com/tolstislon/pytest-pytestrail',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pytest>=3.8.0',
        'testrail-api>=1.1.2'
    ],
    include_package_data=True,
    python_requires='>=3.6',
    license='MIT License',
    entry_points={
        'pytest11': ['pytest_pytestrail = pytest_pytestrail.conftest']
    },
    keywords=[
        'testrail',
        'pytest',
        'pytest-testrail',
        'pytest-pytestrail',
        'testrail_api',
        'api'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
        'Environment :: Plugins',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython'
        'Topic :: Software Development :: Testing'
    ]
)
