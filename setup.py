#!/usr/bin/env python

##############################################################################
#
# UMDInst setup script
#
##############################################################################

"""
Setup script

  Installation

    This builds python modules and installs everything needed to support
    umdinst. For example...

      python setup.py install --mode=prof
"""

import sys
import os
from distutils.core import setup, Extension
from distutils.command.build_scripts import build_scripts
from distutils.command.install import install, INSTALL_SCHEMES
from distutils.dist import Distribution

# Fix for older versions of Python
try:
    True
except NameError:
    True,False = 1,0

class MyDistribution (Distribution):
    def __init__(self, *attrs):
        Distribution.__init__(self, *attrs)
        self.cmdclass['install'] = UMDInstInstall
        self.cmdclass['build_scripts'] = UMDInstBuildScripts

class UMDInstInstall (install):
    user_options = [
        ('mode=', None, "instrumentation mode ('prof', 'ind', 'full', 'none')"),
        ('id=', None, "identifier used to refer to this class or study"),
        ('with-pooledlog', None, "enable the logging to observer's directory"),
        ('without-pooledlog', None, "disable the logging to observer's directory"),
        ('with-privatelog', None, "enable the loging to subject's home directory"),
        ('without-privatelog', None, "disable the loging to subject's home directory"),
        ('with-privatecvs', None, "enable the loging to private cvs"),
        ('without-privatecvs', None, "disable the loging to private cvs"),
        ('with-workflow', None, "enable the online workflow functionality"),
        ('without-workflow', None, "disable the online workflow functionality"),
        ('with-hackystat', None, "enable Hackystat (default)"),
        ('without-hackystat', None, "disable Hackystat"),
        ('hackystat-host=', None, "Hackystat server URL"),
        ('javapath=', None, "Java executable to be used by Hackystat"),
        ('target-batches=', None, "batch queue submision programs to instrument"),
        ('target-compilers=', None, "compilers to instrument"),
        ('target-debuggers=', None, "debuggers to instrument"),
        ('target-interactives=', None, "interactive job submision programs to instrument"),
        ('target-profile-reporter=', None, "profile reporter to instrument"),
        ('target-profiler=', None, "profiler to instrument"),
        ('profiler-outputfile=', None, "profiler output file"),
        ('encoding=', None, "encoding of the log file (base64, quopri, raw)"),
        ('skip-permcheck', None, "skip checking of the directory permissions (for testing purpose only)"),
        ] + install.user_options
    boolean_options = [
        'with-hackystat',
        'with-pooledlog',
        'with-privatelog',
        'with-privatecvs',
        'with-workflow',
        'skip-permcheck',
        ] + install.boolean_options
    negative_opt = {'without-hackystat' : 'with-hackystat',
                    'without-pooledlog' : 'with-pooledlog',        
                    'without-privatelog' : 'with-privatelog',
                    'without-privatecvs' : 'with-privatecvs',
                    'without-workflow' : 'with-workflow',
                    }
    # The following 3 options are initialized to '-1' to allow the
    # mode definition to be overwritten with these options. A dirty hack...
    with_pooledlog = -1
    with_privatelog = -1
    with_privatecvs = -1
    mode = ''
    id = None
    with_workflow = False
    with_hackystat = True
    hackystat_host=None
    javapath=None
    target_compilers=None
    target_batches=None
    target_interactives=None
    target_debuggers=None
    target_profile_reporter=None
    target_profiler=None
    profiler_outputfile=None
    additional_path=None
    keyfile=None
    whitelistfile=None
    encoding = 'base64'
    skip_permcheck=False
    # Options reserved for future
    #target_makes=/usr/bin/make
    #inst_classid=ChangeMeToYourClassID
    #inst_upload_host=care.cs.umd.edu:8080
    #inst_upload_path=/cgi-bin/test/up.cgi

    def run(self):
        # Determine data recording mode
        if self.encoding != 'base64' and self.encoding != 'quopri' and self.encoding != 'raw':
            print 'Error: encoding mode must be one of base64, quopri or raw.'
            sys.exit(-1)
        # Class/study identifier
        if self.id is None:
            print 'Error: class/study identified must be specified with --id option'
            sys.exit(-1)
        # Explicit logging option (--with-xx, --without-xxx) has a priority
        if self.mode == 'prof':
            if self.with_pooledlog == -1: self.with_pooledlog = True
            if self.with_privatelog == -1: self.with_privatelog = False
            if self.with_privatecvs == -1: self.with_privatecvs = False
        elif self.mode == 'ind':
            if self.with_pooledlog == -1: self.with_pooledlog = False
            if self.with_privatelog == -1: self.with_privatelog = True
            if self.with_privatecvs == -1: self.with_privatecvs = True
        elif self.mode == 'full':
            if self.with_pooledlog == -1: self.with_pooledlog = True
            if self.with_privatelog == -1: self.with_privatelog = True
            if self.with_privatecvs == -1: self.with_privatecvs = True
        elif self.mode == 'none':
            if self.with_pooledlog == -1: self.with_pooledlog = False
            if self.with_privatelog == -1: self.with_privatelog = False
            if self.with_privatecvs == -1: self.with_privatecvs = False
        else:
            print '''Error: --mode option must be specified with a valid recording mode.
  --mode=prof: use pooled-logging (store log files in professor/TA\'s directory)
  --mode=ind:  use private-logging (store a log file in individual subject\'s directory)
  --mode=none: disable all data logging features (nothing is recorded by default)
  --mode=full: enable all data logging features
Individual data logging features can be enabled/disabled by specifying 
 --with-XX and/or --without-XX after the --mode option.
See the output of "python setup.py --help" for detailed information.'''
            sys.exit(-1)
        if self.with_pooledlog:
            print 'Enabling pooled logging'
        if self.with_privatelog:
            print 'Enabling private logging'
        if self.with_privatecvs:
            print 'Enabling cvs logging'
        if self.with_workflow:
            print 'Enabling onling workflow tool'
        if not self.skip_permcheck:
            if self.with_pooledlog or self.mode is 'prof':
                print 'Checking the directory permission'
                from umdinst.setup import verifyperms
                verifyperms.check(os.path.abspath(self.prefix))
        from distutils.dir_util import mkpath
        # FIXME: is there a better way to guarantee that the install dir
        # has the right permission?
        mkpath(self.prefix)
        os.chmod(self.prefix, int('755', 8))
        install.run(self)

class UMDInstBuildScripts (build_scripts):
    def createdir(self, dirname):
        """Create a directory and set permissions"""
        try:
            os.stat(dirname) # Will raise OSError if the file doesn't exist
            if not os.path.isdir(dirname):
                raise ValueError, "%s was specified as a directory, but it is not a directory" % mode
        except OSError:
            print "Directory %s does not exist, creating" % dirname
            #os.mkdir(dirname)
            os.makedirs(dirname)

    def run(self):
        from umdinst.setup import gen_config, gen_wrappers
        env = self.distribution.get_command_obj('install')
        # First, check to make sure the javapath is valid
        if env.with_hackystat:
            if (env.javapath is not None) and (env.javapath is not '') and not os.access(env.javapath,os.X_OK):
                #raise ValueError, "Could not find java executable in 'javapath' specified in config: " + env.javapath + "\nSpecify a valid java executable with the '--javapath=' option or disable Hackystat with the '--without-hackystat' option."
                print "Error: could not find java executable in 'javapath' specified in config: " + env.javapath + "\nSpecify a valid java executable with the '--javapath=' option or disable Hackystat with the '--without-hackystat' option."
                sys.exit(-1)

        # Sanity check, make sure there's a keyfile, or setup will fail for now
        if(not os.path.exists(os.path.join('conf', env.keyfile))):
            raise ValueError, "Cannot locate keyfile (%s) which is needed for installation." % env.keyfile

        # Sanity check, make sure there's a askfile, or setup will fail for now
        if(not os.path.exists(os.path.join('conf', env.whitelistfile))):
            raise ValueError, "Cannot locate askfile (%s) which is needed for installation." % env.whitelistfile

        # Generate the config file for runtime
        platform_specific_file = os.path.join('scripts','wrapper','platform_specific.py')
        gen_config.gen_platform_specific_config(env, platform_specific_file)

        # Generate the wrapper scripts
        absprefix = os.path.abspath(env.prefix)
        version = '%d.%d' % sys.version_info[:2]
        libpath = '''%s/lib/python%s/site-packages''' % (absprefix, version)
        gen_wrappers.gen_wrappers(env, libpath)

        if env.with_pooledlog:
            logfiledir = os.path.join(absprefix, '.data')
            self.createdir(logfiledir)
            from stat import S_IRWXU, S_IRWXG, S_IRWXO
            os.chmod(logfiledir, S_IRWXU | S_IRWXG | S_IRWXO)
            print '''changing mode of %s to 777 for pooled logging''' % logfiledir

        #from umdinst.setup import autobackup
        #autobackup.launch_backup_daemon()

        # Finally, a dirty trick to add dynamically generated scripts
        # to the script list
        self.scripts = self.scripts + ['scripts/wrapper/' + x for x in
         os.listdir ('scripts/wrapper/') if not os.path.isdir(x)]

        # Run the default build_script.run() method
        build_scripts.run(self)

setup(name = 'umdinst',
      version = '2.0.3',
      author = ['Lorin Hochstein', 'Taiga Nakamura'],
      author_email = ['lorin@cs.umd.edu', 'nakamura@cs.umd.edu'],
#      maintainer = 'Experimental Software Engineering Group at University of Maryland',
#      maintainer_email= 'eseg@care.cs.umd.edu',
      url = 'http://www.cs.umd.edu/projects/SoftEng/ESEG/',
      description = 'Instrumentation for productivity experiments',
      packages = ['umdinst'],
      scripts = ['scripts/misc/backup.py', 'scripts/misc/upload.py',
                 'scripts/misc/logify', 'scripts/misc/run'],
      # FIXME: "ask.txt" and "keys.txt" shouldn't be hardcoded
      data_files = [('lib', ['jarlib/hackyInstaller.jar']),
                    ('share/umdinst', ['conf/ask.txt', 'conf/keys.txt'])],
      distclass = MyDistribution,
      )
