# #######################################################################################
# ---------------------------------------------------------------------------------------
# File:   setup.py
# Author: Luis Monteiro
# ---------------------------------------------------------------------------------------
# #######################################################################################
# imports
from setuptools import setup, find_packages
# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------
with open('readme.md', 'r') as fh:
    long_description = fh.read()
# -----------------------------------------------------------------------------
# setup
# -----------------------------------------------------------------------------
setup(
    name='terminator',  
    version='0.3',
    author='Luis Monteiro',
    author_email='monteiro.lcm@gmail.com',
    description='Interface for command line',
    long_description=long_description,
    packages=[
        'terminator',
        'terminator.extensions',
    ],
    install_requires=[
        # framework
        'robotworker @ git+https://nearshore.altran.pt/git/altran_v_v/robot-libraries/robotworker.git',
        # community
        'gitpython',
        'parse'
    ],
    entry_points={
      'console_scripts': [
          'terminator = terminator.worker:main',
      ]
    }
 )
# #######################################################################################
# ---------------------------------------------------------------------------------------
# End
# ---------------------------------------------------------------------------------------
# #######################################################################################