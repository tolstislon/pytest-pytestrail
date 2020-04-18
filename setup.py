from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent.absolute().joinpath('README.md')
with readme_file.open(encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='pytest-pytestrail',
    description='Pytest plugin for interaction with TestRail',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='tolstislon',
    author_email='tolstislon@gmail.com',
    url='https://github.com/tolstislon/pytest-pytestrail',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pytest>=3.8.0',
        'testrail-api>=1.5.0'
    ],
    include_package_data=True,
    use_scm_version={"write_to": "pytest_pytestrail/__version__.py"},
    setup_requires=['setuptools_scm'],
    python_requires='>=3.6',
    license='MIT License',
    entry_points={
        'pytest11': ['pytest_pytestrail = pytest_pytestrail.plugin']
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
