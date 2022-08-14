import os

from setuptools import setup, find_packages


with open('VERSION', 'r') as f:
    version = f.read().rstrip()

with open('requirements.txt') as f:
    install_requires = [l.strip() for l in f]


python_requires = '>=3.8'

tests_require = [
    'black',
    'pytest',
    'pytest-cov',
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''


setup(
    name='citytetris',
    version=version,
    description="Tetris with a twist",
    long_description=README,
    license='new BSD 3-Clause',
    packages=find_packages(),
    include_package_data=True,
    python_requires=python_requires,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
    },
)
