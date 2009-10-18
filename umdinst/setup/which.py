#!/bin/env python
#
# Implements the "which" tcsh command in Python

import os

def is_executable(filename):
    return os.access(filename, os.X_OK)    

def which(app):
    dirnames = os.environ["PATH"].split(os.path.pathsep)
    for dirname in dirnames:
        filename = os.path.join(dirname, app)
        if (os.access(filename, os.X_OK) and os.path.isfile(filename)): 
            return filename
    return None

