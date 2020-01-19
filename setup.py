from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='IL Tokenizer',
      version='0.0.1',
      install_requires=requirements,
      description='Tokenizer for English and ILs',
      packages=['ilstokenizer'])
