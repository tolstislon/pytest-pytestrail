from pathlib import Path

from setuptools import find_packages, setup

import pytest_pytestrail

readme_file = Path(__file__).parent.absolute().joinpath('README.md')
with readme_file.open(encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='pytest-pytestrail',
    description=pytest_pytestrail.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=pytest_pytestrail.__version__,
    author=pytest_pytestrail.__author__,
    author_email=pytest_pytestrail.__author_email__,
    url=pytest_pytestrail.__url__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pytest>=3.8.0',
        'testrail-api>=1.5.0'
    ],
    include_package_data=True,
    python_requires='>=3.6',
    license=pytest_pytestrail.__license__,
    entry_points={
        'pytest11': [
            'pytest_pytestrail = pytest_pytestrail.conftest'
        ]
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
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance'
    ]
)
