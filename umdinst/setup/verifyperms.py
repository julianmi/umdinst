#!/usr/bin/env python

import os
from stat import *

def parent(path):
    """Return the parent of the specified directory"""
    # Remove the trailing slash, if any
    if path.endswith('/'):
        return os.path.dirname(path[:-1])
    else:
        return os.path.dirname(path)
    
def create_and_set_permissions(dirname,perms):
    """Create a directory and set permissions"""
    try:
        os.stat(dirname) # Will raise OSError if the file doesn't exist
        if not os.path.isdir(dirname):
            raise ValueError, "%s was specified as a directory, but it is not a directory" % mode
    except OSError:
        print "Directory %s does not exist, creating" % dirname
        #os.mkdir(dirname)
        os.makedirs(dirname)
    # Set permissions on the directory directory
    os.chmod(dirname,perms)

def check_parent_permissions(dirname,perms):
    """Check the permissions of the directory  its parents to
    make sure the appropriate permissions are there."""
    pathname = dirname
    while(pathname != ''):
        st = os.stat(pathname)
        dirperms = S_IMODE(st[ST_MODE])
        if  (dirperms & perms) < perms:
            #raise ValueError, pathname + " does not have the right permissions."
            print '''Error: %s does not have the right permission.
The installation mode specified requires the installation directory
to be readable and executable by other users. Change the permission setting, 
or change the installation directory with the '--prefix' option.''' % pathname
            import sys
            sys.exit(-1)
        pathname = parent(pathname)


def check(installdir):
    # Sanity check, make sure that the directories up to this point have
    # the appropriate permissions
    #
    permissions_are_ok = True

    # User and group read execute
    grp_rx_perms = S_IRWXU | S_IRGRP | S_IXGRP 

    # All user read execute
    all_rx_perms = S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH

    # The parent directories may not actually all have user write access
    # Some systems don't allow all users to access all parent directories,
    # So we change it to checking for group accesses.
    check_perms = grp_rx_perms & ~S_IWUSR

    try:
        check_parent_permissions(parent(installdir),check_perms)
    except OSError, e:
	# I'm going to be naive here and assume that errno's are the same across
	# all systems. Hopefully it's a POSIX thing.
	if e.errno==2: # No such file or directory
	    raise ValueError, "There is a problem with the value for 'installdir' in config.py: " + installdir
	else:
	    permissions_are_ok = False
    #create_and_set_permissions(installdir,all_rx_perms)
    #check_parent_permissions(parent(logfiledir),check_perms)
    #allperms = S_IRWXU | S_IRWXG | S_IRWXO
    #create_and_set_permissions(logfiledir,allperms)

    if not permissions_are_ok:
        print "Warning: Cannot confirm that permissions are set correctly."
        print "Please check to make sure that subjects have read access to umdinst/setup and umdinst/bin, and write accesss to umdinst/.data"
