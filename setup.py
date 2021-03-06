
from setuptools import setup, find_packages

setup(
  name='QuGraphy',
  version='1.0.0',
  author='Mohamed ShehabEldin',
  author_email='mohamed.sami@zewailcity.edu.eg',
  description='''A collection of Python functions to ease and visualise 
  the calculations of Quantum computation and information''',
  packages=['QuGraphy'],
  url='https://github.com/Mohamed-ShehabEldin/QuGraphy',
  install_requires=[
    'qutip',
    'qiskit',
    'numpy',
    'matplotlib'
  ]
)
