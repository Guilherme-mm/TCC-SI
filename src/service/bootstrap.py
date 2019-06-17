"""
@author Guilherme Muller Moreira <guilherme.muller.m@gmail.com>
@version 0.1
@creation 22/04/2019

Description
-----------
    This script is responsible for starting the services that composes the application. It's like a enter point of the system.
"""
import os
import sys

serviceApiPath = os.path.join(os.getcwd(), "api/ServiceAPI.py")

# os.system('{} {} {} {}'.format('python', '-m', 'flask', 'run'))
os.system('{} {}'.format('python', serviceApiPath,))