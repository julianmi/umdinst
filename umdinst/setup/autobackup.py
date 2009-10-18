#!/usr/bin/env python
import os

# Fix for older versions of Python
try:
    True
except NameError:
    True,False = 1,0

def launch_backup_daemon():
    # First, check to see if upload is supported
    try:
        import upload
    except ImportError:
        # OK, upload doesn't work. Now let's see if wget is in the PATH
        pass
    
    # Launch the backup daemon
    print "Launching the auto-upload daemon..."
    os.system("./autobackup.sh start")
    print "Launched (pid in autobackup.pid)"
