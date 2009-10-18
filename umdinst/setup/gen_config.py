import os

# Fix for older versions of Python
try:
    True
except NameError:
    True,False = 1,0

def gen_platform_specific_config(env, platform_specific_file):
    # Generate the config file for runtime
    absprefix = os.path.abspath(env.prefix)
    dirnames = os.path.join(absprefix, 'bin')
    libdir = os.path.join(absprefix, 'lib')
    logfiledir = os.path.join(absprefix, '.data')
    whitelistfile = os.path.join(absprefix, 'share', 'umdinst', env.whitelistfile)
    homelogdir = '~/.umdinst' # should expanded in the runtime script
    privatelogfiledir = os.path.join(homelogdir, 'data')
    keyfile = os.path.join(absprefix, 'share', 'umdinst', env.keyfile)
    sandbox = os.path.join(homelogdir,'sandbox')
    repository = os.path.join(homelogdir,'repository')
    if env.with_pooledlog:
        registerdir = '"' + os.path.join(absprefix, '.data') + '"'
    elif env.with_privatelog:
        registerdir = '"' + homelogdir + '"'
    else:
        registerdir = None
    f = open(platform_specific_file,'w')
    f.write('#!/usr/bin/env python\n')
    f.write('id = "%s"\n' % env.id)
    f.write('logfiledir = "%s"\n' % logfiledir)
    f.write('privatelogfiledir = "%s"\n' % privatelogfiledir)
    f.write('whitelistfile = "%s"\n' % whitelistfile)
    f.write('with_pooledlog = %s\n' % env.with_pooledlog)
    f.write('with_privatelog = %s\n' % env.with_privatelog)
    f.write('with_privatecvs = %s\n' % env.with_privatecvs)
    f.write('with_workflow = %s\n' % env.with_workflow)
    f.write('encoding = "%s"\n' % env.encoding)
    f.write('sandbox = "%s"\n' % sandbox)
    f.write('repository = "%s"\n' % repository)
    f.write('additional_path = "%s"\n' % env.additional_path)
    ## For instrument code
    # Bit of hack here. If the Java path is empty, we don't want it quoted.
    # So we need to create a variable called "quotedjavapath" and quote it if
    # there's a path, otherwise leave it unquoted.
    if (env.javapath is not None) and (env.javapath is not ''):
        quotedjavapath = '"' + env.javapath + '"'
    else:
        quotedjavapath = None
    f.write('''# For instrument setup
dirnames = ["%s"]
keyfile = "%s"
registerdir = %s
javapath = %s
libdir = "%s"
with_hackystat = %s
hackystat_host = "%s"
''' % (dirnames,keyfile,registerdir,quotedjavapath,libdir,env.with_hackystat, env.hackystat_host))
    f.close()

