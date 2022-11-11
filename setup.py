from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='daily',
    version='0.1.0',
    description='Your daily content from multiple sources on one page',
    long_description=readme,
    author='Tom Allen',
    author_email='tswallen@outlook.com',
    url='https://github.com/tswallen/the-daily',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

