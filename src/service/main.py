"""
@author Guilherme Muller Moreira <guilherme.muller.m@gmail.com>
@version 0.1
@creation 16/07/2019

Description
-----------
    This module is the entry point for the serviec execution.
"""

from pkg.api.ServiceAPI import ServiceAPI

if __name__ == '__main__':
    SERVICEAPI = ServiceAPI()
    SERVICEAPI.run()
