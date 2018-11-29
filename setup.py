from setuptools import setup
import pytest_pytestrail

with open('readme.rst', 'r') as file:
    long_description = file.read()

setup(
    name='pytest-pytestrail',
    description='pytest plugin for interaction with TestRail',
    long_description=long_description,
    version=pytest_pytestrail.__version__,
    author='tolstislon',
    author_email='tolstislon@gmail.com',
    url='https://github.com/tolstislon/pytest-pytestrail',
    packages=['pytest_pytestrail'],
    install_requires=['pytest>=4.0.1', 'testrail-api>=1.0.0', 'colorama>=0.4.1'],
    include_package_data=True,
    python_requires='>=3.6',
    license='MIT License',
    entry_points={'pytest11': ['pytest_pytestrail = pytest_pytestrail.conftest']},
    keywords=['testrail', 'pytest', 'pytest-testrail', 'pytest-pytestrail', 'testrail_api'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing'
    ]
)
