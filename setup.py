from setuptools import setup, find_packages
from os.path import exists
# Function to read the requirements file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if not line.startswith('#')]

setup(
    author="Bishoy",
    name='pieces autocommit',
    url='https://github.com/BishoyHanyRaafat/autocommit/',
    version='0.1.0',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    long_description=open('README.md').read() if exists('README.md') else '',
    entry_points={
        'console_scripts': ['autocommit = src.__main__:main']
    },
    python_requires=">=3.9",
    keywords=['CLI', 'cli', 'autocommit', 'autocommit-cli', 'autocommit-client', 'autocommit-client-cli'],
    classifiers=['Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Intended Audience :: Developers',
                 'Environment :: Console'
                 ],
    platforms=['ALL'],
)