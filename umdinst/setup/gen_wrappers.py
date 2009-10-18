import os
import re

# Fix for older versions of Python
try:
    True
except NameError:
    True,False = 1,0

def write_file(fname, s):
    f = open(fname,'w')
    f.write(s)
    f.close()

def gen_wrappers(env, libpath):
    '''Generate wrapper scripts'''
    # Wrap the compilers
    for compiler in env.target_compilers.split(':'):
        if compiler is not '':
            print "Wrapping " + compiler
            if(re.match('\$HOME/', compiler)):
                compilername = "os.environ['HOME'] +" + '"' + compiler[5:] + '"'
            else:
                compilername = '"' + compiler + '"'
            s = open(os.path.join('conf', 'compiler.py.in')).read() % (libpath, compilername)
            fname = os.path.join('scripts','wrapper',os.path.basename(compiler))
            write_file(fname, s)
    # Wrap the batch job schedulers
    for runprog in env.target_batches.split(':'):
        if runprog is not '':
            print "Wrapping " + runprog
            if(re.match('\$HOME/', runprog)):
                runprogname = "os.environ['HOME'] +" + '"' + runprog[5:] + '"'
            else:
                runprogname = '"' + runprog + '"'
            s = open(os.path.join('conf', 'run_batch.py.in')).read() % (libpath, runprogname)
            fname = os.path.join('scripts','wrapper',os.path.basename(runprog))
            write_file(fname, s)
    # Wrap the interactive job schedulers
    for runprog in env.target_interactives.split(':'):
        if runprog is not '':
            print "Wrapping " + runprog
            if(re.match('\$HOME/', runprog)):
                runprogname = "os.environ['HOME'] +" + '"' + runprog[5:] + '"'
            else:
                runprogname = '"' + runprog + '"'
            s = open(os.path.join('conf', 'run_interactive.py.in')).read() % (libpath, runprogname)
            fname = os.path.join('scripts','wrapper',os.path.basename(runprog))
            write_file(fname, s)
    # Wrap the debuggers
    for debugger in env.target_debuggers.split(':'):
        if debugger is not '':
            print "Wrapping " + debugger
            if(re.match('\$HOME/', runprog)):
                debuggername = "os.environ['HOME'] +" + '"' + debugger[5:] + '"'
            else:
                debuggername = '"' + debugger + '"'
            s = open(os.path.join('conf', 'debugger.py.in')).read() % (libpath, debuggername)
            fname = os.path.join('scripts','wrapper',os.path.basename(debugger))
            write_file(fname, s)
    # Wrap the profiler
    if (env.target_profiler is not None) and (env.target_profiler is not ''):
	print "Wrapping " + env.target_profiler
        if(re.match('\$HOME/', env.target_profiler)):
            target_profilername = "os.environ['HOME'] +" + '"' + env.target_profiler[5:] + '"'
        else:
            target_profilername = '"' + env.target_profiler + '"'
        s = open(os.path.join('conf', 'profiler.py.in')).read() % (libpath, target_profilername, env.profiler_outputfile)
        fname = os.path.join('scripts','wrapper',os.path.basename(env.target_profiler))
        write_file(fname, s)
    # Wrap the profile reporter
    if (env.target_profile_reporter is not None) and (env.target_profile_reporter is not ''):
        print "Wrapping " + env.target_profile_reporter
        if(re.match('\$HOME/', env.target_profile_reporter)):
            target_profile_reportername = "os.environ['HOME'] +" + '"' + env.target_profile_reporter[5:] + '"'
        else:
            target_profile_reportername = '"' + env.target_profile_reporter + '"'
        s = open(os.path.join('conf', 'profiler_reporter.py.in')).read() % (libpath, target_profile_reportername)
        fname = os.path.join('scripts','wrapper',os.path.basename(env.target_profile_reporter))
        write_file(fname, s)
