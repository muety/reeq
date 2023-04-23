#!/usr/bin/env python

# https://packaging.python.org/tutorials/packaging-projects/
# pip install wheel auditwheel
# python setup.py sdist bdist_wheel
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*.tar.gz dist/*win_*.whl dist/manylinux/*.whl

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='reeq',
    version='0.2.0',
    description='An extremely simple, minimalistic library for handling events published to Redis.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ferdinand Mütsch',
    author_email='ferdinand@muetsch.io',
    url='https://github.com/muety/reeq',
    packages=['reeq'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Cython',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'System :: Distributed Computing'
        'Typing :: Typed'
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/muety/reeq/issues',
        'Source Code': 'https://github.com/muety/reeq',
    },
    python_requires='>=3.9',
    install_requires=['redis']
)
