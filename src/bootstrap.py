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

#===== Daemon Service Start ====
# print("starting the recommendation app...")
# sys.stdout.flush() #just to assure the print output order

#mounting the path to the main controller script
# cwd = os.path.join(os.getcwd(), "service/api/ServiceAPI.py")

#executing the main controller script via OS handling to simulate a systemd call
# os.system('{} {} {}'.format('python', cwd, "start"))

#===== Service API Boot Up =====
print("starting the service API...")
sys.stdout.flush()
# Gets the path to the api that will be available to cli tools client
serviceApiPath = os.path.join(os.getcwd(), "service/api/ServiceAPI.py")

# Flask will search the app based on a env variable. This line informs the API code path to flask
os.environ['FLASK_APP'] = serviceApiPath

# Starts flask!
os.system('{} {} {} {}'.format('python', '-m', 'flask', 'run'))