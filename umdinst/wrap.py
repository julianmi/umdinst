#!/usr/bin/env python
import commands
import os
import popen2
import quopri
import base64
import re
import shutil
import string
import sys
import time


# Fix for older versions of Python
try:
    True
except NameError:
    True,False = 1,0
    


# Singleton-like design pattern
# See: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531
# class Constants:
#     __shared_state = {}
#     def __init__(self):
#         self.__dict__ = self.__shared_state

# Import platform_specific data
import platform_specific

def printable(s):
    "Convert a string to only printable characters"

    # Apparently, the last two characters in string.printable are not XML-friendly
    # This code could be problematic if string.printable's order varies by machine
    return ''.join([c for c in s if c in string.printable[:98]])



def run(prog,args):
    """Run a program and return true if succeeds, false if fails

    prog: Name of the program 
    args: List of command-line arguments"""
    status = os.spawnv(os.P_WAIT,prog,[prog] + args)
    success = os.WIFEXITED(status) and os.WEXITSTATUS(status)==0
    return success

def getlogin():
    """Return the name of the login
    
    We try several things until something works"""
    try:
        return os.environ['USER']
    except:
        try:
            return os.environ['LOGNAME']
        except:
            try:
                import pwd
                return pwd.getpwuid(os.getuid())[0]
            except:
                return os.getlogin()
            

def hasextension(fname):
    """Check if a filename has an extension"""
    return fname.find('.')!=-1

def issourcefile(fname):
    """Check if the file name corresponds to a source file.

    For now, all files that have an extension that isn't .exe or .a or .o"""
    return hasextension(fname) and True not in [fname.endswith(x) for x in ['.o','.exe','.a'] ]

def getlogfilepath(logfiledir):
    """Return the full path of the logfile"""
    return os.path.join(logfiledir,getlogin() + '.log')

def getcommand(argv):
    """Retrieve a string version of the command that was invoked at the shell

    We can't get it exactly because the shell does substitutions on the
    command-line arguments."""
    return ' '.join(argv)

# Parse through source code and retrieve headers
headerpat = re.compile(r'#include[ \t]+"(.*)"') 

def parseheaders(source):
    """Extract the names of local header files from source code. Not smart enough to deal
    with comments"""
    return headerpat.findall(source)

def unique(alist):
    """Return unique elements from a list.

    Taken from comments in  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52560"""
    myset = {}
    return [myset.setdefault(e,e) for e in alist if e not in myset]

def flatten(alist):
    """Flatten a list. Each element in the list must itself be a list"""
    return [x for y in alist for x in y]

def encode(string, encoding):
    if encoding == 'quopri':
        return quopri.encodestring(string)
    elif encoding == 'base64':
        return base64.encodestring(string)
    elif encoding == 'raw':
        return string
    else:
        return string

class CVSUtils:
    """Interacts with CVS."""

    def __init__(self,sandbox,commitmsg):
	"""sandbox - CVS sandbox directory which will be used for commits"""
	self.sandbox = sandbox
        self.commitmsg = commitmsg
    
    def commit_files_to_cvs(self,files):
	""" Commit the sourcefiles and headerfiles to CVS"""

	for f in files:
	    self._copy_to_sandbox(f)
	self._commit_sandbox_files()

    def _copy_to_sandbox(self,fname):
	""" Copy a file to the sandbox, creating directories and adding to CVS when necessary.
	Does not do a commit"""
        dest = self._change_base_directory(os.path.abspath(fname),self.sandbox)
	self._check_and_create_dir(os.path.dirname(dest))
	shutil.copy(fname,dest)
	# We don't always need to add the file, but it's easier to try and add it every time
	(status,output) = commands.getstatusoutput("cd %s ; cvs add %s" % (self.sandbox,dest))
	if status!=0:
            # Only complain if it's not an "already exists" problem
            if output.find('already exists')==-1: 
                raise ValueError, "Could not add file %s: %s" % (dest,output)

    def _check_and_create_dir(self,dirname):
	"""Check if a directory exists, and if not, create it in the sandbox and and commit it.

	The directory must be within the sandbox"""
	if not os.path.exists(dirname):
	    # If it's not there, check the parent directory
	    self._check_and_create_dir(os.path.dirname(dirname))
	    os.mkdir(dirname)
	    rel_dirname = self._relative_path(dirname,self.sandbox)
	    (status,output) = commands.getstatusoutput("cd % s ; cvs add %s " % (self.sandbox,rel_dirname))
	    if status!=0:
		raise ValueError, "Could not add directory %s: %s" % (dirname,output)

    def _commit_sandbox_files(self):
	"""Commits all of the files currently in the sandbox.

	Returns the output of the CVS commit command"""
        #return commands.getoutput("cd %s ; cvs commit -f -R -m ' ' ." % self.sandbox)
        return commands.getoutput("cd %s ; cvs commit -m '%s' ." % (self.sandbox, self.commitmsg))

    def gethomepaths(self):
        """ Get the list of home directory paths. Some environments have
        a number of different absolute paths mapped to the use home directory,
        which becomes an issue when capturing the code to cvs.
        It typically happens when the value of $HOME is different from 
        the standard naming convention on the filesystem.
        The method used here is a little hackyish.
        """
        cwd = os.getcwd()
        home_dir = os.path.expanduser('~')
        os.chdir(home_dir)
        fs_dir = os.path.abspath('.')
	os.chdir(cwd) # I hope this will always get you back to the original place...
        if home_dir!= fs_dir:
            return [home_dir, fs_dir]
        else:
            return [home_dir]

    def _change_base_directory(self,fname,basename):
	""" Change the base directory of fname from oldbase to newbase

        Absolute path of files must be used!"""

        # Compensate the possible problem with incompatible HOME paths
        bases = self.gethomepaths()
        for base in bases:
            if os.path.commonprefix([fname,base]) == base:
                fname = fname.replace(base, '/_HOME', 1)
        # Drop leading delimiter
        # FIXME: the following line is not portable...
	return os.path.join(basename, fname[1:])

    def _relative_path(self,fname,base):
	"""Create a relative path from an absolute and a base"""
	
	if os.path.commonprefix([fname,base])!=base:
	    raise ValueError, "Unexpected base in file" + fname


	# Make sure base ends in a slash, or the following will fail
	if base[-1] != '/':
	    base = base + '/'
	return fname.replace(base,'')
	

class CompileData:
    """Holds data associated with a compile"""
    def __init__(self,starttime,endtime,sourcefiles,subject,command,success,path,debugging=None,cvs=None):
        self.timestamp = starttime
        self.timestr = time.ctime(self.timestamp)
        self.sourcefiles = sourcefiles
        self.subject = subject
        self.command = command
        self.time_interval = endtime-starttime
	self.success = success
	self.path = path
	self.debugging = debugging
        self.cvs = cvs
        self.encoding = platform_specific.encoding # 'base64', 'quopri' or 'raw'

        self.headerfiles = []

        # Determine the headerfiles
        for sourcefile in self.sourcefiles:
            srcdir = os.path.dirname(sourcefile)
            candidates = parseheaders(open(sourcefile).read())
            for h in candidates:
                headerpath = os.path.join(srcdir,h)
                if os.path.exists(headerpath):
                    self.headerfiles.append(headerpath)


    def getcvscomment(self):
	cxml_cvs = '''<compile success="%(success)d" %(debug)s>
<timestr>%(timestr)s</timestr>
<time_interval>%(time_interval).2f</time_interval>
</compile>
'''
	if self.debugging is not None:
	    debug = 'debugging="%d"' % self.debugging
	else:
	    debug = ''
	return cxml_cvs % {
		    'timestr' : self.timestr,
		    'command' : self.command,
                    'success' : self.success,
		    'debug' : debug,
                    'time_interval' : self.time_interval
                    }


    def addtocvs(self,sandbox):
        """Add the files to the CVS repository.

        sandbox - location of CVS sandbox where files need to be copied and committed."""
        commitmsg = self.getcvscomment()
        cvs = CVSUtils(sandbox, commitmsg)
        cvs.commit_files_to_cvs(self.sourcefiles+self.headerfiles)
        
    def toxml(self):
	sfxml = '''<sourcefile success="%(success)d">
<name>%(name)s</name>
<time>%(timestamp)d</time>
<timestr>%(timestr)s</timestr>
<subject>%(subject)s</subject>
<command><![CDATA[%(command)s]]></command>
<time_interval>%(time_interval).2f</time_interval>
<path>%(path)s</path>
<source encode="%(encoding)s"><![CDATA[%(source)s]]></source>
</sourcefile>
'''
	hfxml = '''<headerfile>
<name>%(name)s</name>
<time>%(timestamp)d</time>
<timestr>%(timestr)s</timestr>
<subject>%(subject)s</subject>
<command><![CDATA[%(command)s]]></command>
<time_interval>%(time_interval).2f</time_interval>
<path>%(path)s</path>
<source encode="%(encoding)s"><![CDATA[%(source)s]]></source>
</headerfile>
'''

	cxml = '''<compile success="%(success)d" %(debug)s>
<time>%(timestamp)d</time>
<timestr>%(timestr)s</timestr>
<subject>%(subject)s</subject>
<command><![CDATA[%(command)s]]></command>
<time_interval>%(time_interval).2f</time_interval>
</compile>
'''

	if self.debugging is not None:
	    debug = 'debugging="%d"' % self.debugging
	else:
	    debug = ''
	
	return '\n'.join([cxml %  {
		    'timestamp' : self.timestamp,
		    'timestr' : self.timestr,
		    'subject' : self.subject,
		    'command' : self.command,
                    'success' : self.success,
		    'debug' : debug,
			'time_interval' : self.time_interval}] + 
			 [sfxml % {'name' : name,
				   'success' : self.success,
				   'timestamp' : self.timestamp,
				   'timestr' : self.timestr,
				   'subject' : self.subject,
				   'command' : self.command,
				   'time_interval' : self.time_interval,
				   'path' : self.path,
                                   'encoding' : self.encoding,
                                   'source' : encode(open(name).read(), self.encoding)}
			  for name in self.sourcefiles] +
			 [hfxml % {'name' : name,
				   'timestamp' : self.timestamp,
				   'timestr' : self.timestr,
				   'subject' : self.subject,
				   'command' : self.command,
				   'time_interval' : self.time_interval,
				   'path' : self.path,
                                   'encoding' : self.encoding,
				   'source' : encode(open(name).read(), self.encoding)}
			  for name in self.headerfiles])

def set_compiler_invoked():
    os.environ['UMDINST_COMPILER_INVOKED']="1"

def compiler_already_invoked():
    try:
        val = os.environ['UMDINST_COMPILER_INVOKED']
        return True
    except KeyError:
        return False

def ask_if_debugging():
    c = ''
    while c not in ['y','n']:
	c = raw_input("Are you debugging? [y/n]: ").lower()
    return c=='y'

def is_in_whitelist(subject,whitelistfile):
    try:
	approved = [x.rstrip() for x in open(whitelistfile).readlines()]
	return subject in approved
    except TypeError: # whitelistfile==None
	return False


def identify_sourcefiles(args):
    """Identify source files from a list of command-line arguments.

    args - Command-line arguments (does not include name of program)"""

    # If there's a -o and a filename, remove it
    try:
        ind = args.index('-o')
        del args[ind+1]
    except:
        pass


    # Return all arguments that don't start with -, that are sourcefiles, and that are accessible
    return [fname for fname in args if fname[0]!='-' and issourcefile(fname) and os.access(fname,os.R_OK)]
    

def capture_compile(compiler,argv=sys.argv,logex=None):
    """Capture information associated with a compile.

    Return true if compile succeeded, else false"""
    sandbox=os.path.expanduser(platform_specific.sandbox)
    whitelistfile=platform_specific.whitelistfile #os.path.expanduser(platform_specific.whitelistfile)
    starttime = time.time()
    args = argv[1:]
    success = run(compiler,args)
    # If compile succeeded, ask if debugging
    subject = getlogin()
    if success and is_in_whitelist(subject,whitelistfile):
	is_debugging = ask_if_debugging()
    else:
	is_debugging = None
    endtime = time.time()
    c = CompileData(starttime=starttime,
                    endtime=endtime,
                    sourcefiles=identify_sourcefiles(args),
                    subject=subject,
                    command=' '.join(argv),
                    success=success,
		    path = os.getcwd(),
		    debugging=is_debugging)
    if platform_specific.with_privatecvs:
        #print "Writing to CVS..."
        if sandbox is not None:
            c.addtocvs(sandbox) # Add the files to CVS
    if platform_specific.with_privatelog:
        #print "Writing to Private logfile..."
        logfile = getlogfilepath(os.path.expanduser(platform_specific.privatelogfiledir))
        f = open(logfile,'a')
        f.write(c.toxml())
        f.close()
    if platform_specific.with_pooledlog:
        #print "Writing to Pooled logfile..."
        logfile = getlogfilepath(platform_specific.logfiledir)
        f = open(logfile,'a')
        f.write(c.toxml())
        f.close()
        os.chmod(logfile,0644)
    if logex is not None:
        logfile = logex
        f = open(logfile,'a')
        f.write(c.toxml())
        f.close()
        os.chmod(logfile,0644)
    if platform_specific.with_workflow:
        print "Invoking the online workflow tool..."
    return success

def capture_interactive_run(runprog,argv=sys.argv,logex=None):
    """Capture information associated with an interactive run

    Return true if run succeeded, else false"""
    starttime = time.time()
    args = argv[1:]
    success = run(runprog,args)
    endtime = time.time()
    ir = InteractiveRunData(starttime=starttime,
			    endtime=endtime,
			    subject=getlogin(),
			    command=getcommand(argv),
			    success=success,
			    path=os.getcwd())
    if platform_specific.with_privatelog:
        logfile = getlogfilepath(os.path.expanduser(platform_specific.privatelogfiledir))
        f = open(logfile,'a')
        f.write(ir.toxml())
        f.close()
    if platform_specific.with_pooledlog:
        logfile = getlogfilepath(platform_specific.logfiledir)
        f = open(logfile,'a')
        f.write(ir.toxml())
        f.close()
        os.chmod(logfile,0755)
    if logex is not None:
        logfile = logex
        f = open(logfile,'a')
        f.write(ir.toxml())
        f.close()
        os.chmod(logfile,0755)
    return success

def capture_batch_run(runprog,argv=sys.argv,logex=None):
    """Capture information associated with a bactch run

    Return true if run succeeded, else false"""
    starttime = time.time()
    args = argv[1:]
    success = run(runprog,args)
    endtime = time.time()
    # Identify which file is the script file
    fnames = [fname for fname in args if os.access(fname,os.R_OK)]
    # There should only be either 1 or 0 args
    # if there are more than one, just take the first
    if len(fnames)>0:
	fname = fnames[0]
	script = open(fname).read()
    else:
	script = ''
    
    br = BatchRunData(starttime=starttime,
		      endtime=endtime,
		      script=script,
		      subject=getlogin(),
		      command=getcommand(argv),
		      success=success,
		      path=os.getcwd())
    if platform_specific.with_privatelog:
        logfile = getlogfilepath(os.path.expanduser(platform_specific.privatelogfiledir))
        f = open(logfile,'a')
        f.write(br.toxml())
        f.close()
    if platform_specific.with_pooledlog:
        logfile = getlogfilepath(platform_specific.logfiledir)
        f = open(logfile,'a')
        f.write(br.toxml())
        f.close()
        os.chmod(logfile,0755)
    if logex is not None:
        logfile = logex
        f = open(logfile,'a')
        f.write(br.toxml())
        f.close()
        os.chmod(logfile,0755)
    return success

def capture_profiled_run(runprog,outfile,argv=sys.argv,logex=None):
    """Capture information associated with an interactive run

    Return true if run succeeded, else false"""
    starttime = time.time()
    args = argv[1:]
    success = run(runprog,args)
    endtime = time.time()

    # If the file can't be read, just keep the field blank
    try:
	profiledata=open(outfile).read()
    except:
	profiledata = ' '
	    
    pr = ProfileRunData(starttime=starttime,
			endtime=endtime,
			subject=getlogin(),
			command=getcommand(argv),
			success=success,
			path=os.getcwd(),
			profiledata=profiledata)
    if platform_specific.with_privatelog:
        logfile = getlogfilepath(os.path.expanduser(platform_specific.privatelogfiledir))
        f = open(logfile,'a')
        f.write(pr.toxml())
        f.close()
    if platform_specific.with_pooledlog:
        logfile = getlogfilepath(platform_specific.logfiledir)
        f = open(logfile,'a')
        f.write(pr.toxml())
        f.close()
        os.chmod(logfile,0755)
    if logex is not None:
        logfile = logex
        f = open(logfile,'a')
        f.write(pr.toxml())
        f.close()
        os.chmod(logfile,0755)
    return success

def capture_profile_report(runprog,argv=sys.argv,logex=None):
    """Capture information associated with a profile report generation program

    Return true if run succeeded, else false"""
    starttime = time.time()
    args = argv[1:]
    (status, output) = commands.getstatusoutput(' '.join([runprog]+args))
    endtime = time.time()
    # Send the output to standard out
    print output

    if status==0:
        success = True
    else:
        success = False

    subject = getlogin()

    rep = ProfilerReporterData(starttime=starttime,
                               endtime=endtime,
                               subject=subject,
                               command=' '.join(argv),
                               success=success,
                               path= os.getcwd(),
                               reportdata = output)
    if platform_specific.with_privatelog:
        logfile = getlogfilepath(os.path.expanduser(platform_specific.privatelogfiledir))
        f = open(logfile,'a')
        f.write(rep.toxml())
        f.close()
    if platform_specific.with_pooledlog:
        logfile = getlogfilepath(platform_specific.logfiledir)
        f = open(logfile,'a')
        f.write(rep.toxml())
        f.close()
        os.chmod(logfile,0755)
    if logex is not None:
        logfile = logex
        f = open(logfile,'a')
        f.write(rep.toxml())
        f.close()
        os.chmod(logfile,0755)
    return success

def capture_debugger(debuggerprog,argv=sys.argv,logex=None):
    """Capture information associated with a debugger

    Return true if debugger succeeded, else false"""
    starttime = time.time()
    args = argv[1:]
    success = run(debuggerprog,args)
    endtime = time.time()

    subject = getlogin()

    deb = DebuggerData(starttime=starttime,
                       endtime=endtime,
                       subject=subject,
                       command=' '.join(argv),
                       success=success,
                       path=os.getcwd())
    if platform_specific.with_privatelog:
        logfile = getlogfilepath(os.path.expanduser(platform_specific.privatelogfiledir))
        f = open(logfile,'a')
        f.write(deb.toxml())
        f.close()
    if platform_specific.with_pooledlog:
        logfile = getlogfilepath(platform_specific.logfiledir)
        f = open(logfile,'a')
        f.write(deb.toxml())
        f.close()
        os.chmod(logfile,0755)
    return success

    
def capture_make(makeprog,logex=None):
    starttime = time.time()
    args = sys.argv[1:]
    success = run(makeprog,args)
    endtime = time.time()
    c = MakeData(starttime,
                 endtime,
                 get_makefilename(args),
                 getlogin(),
                 ' '.join(sys.argv),
                 success)
    raise ValueError,"This function has not been implemented properly yet!"

class AbstractRunData:
    """Parent class for RunData children

    Children must define a type() method and an extrafields() method"""
    def __init__(self,starttime,endtime,subject,command,success,path):
	self.timestamp = starttime
        self.timestr = time.ctime(self.timestamp)
        self.time_interval = endtime-starttime
	self.subject = subject
	self.command = command
	self.success = success
	self.path = path



    def toxml(self):
	xml = '''<job type="%(type)s" success="%(success)d">
<subject>%(subject)s</subject>    
<time>%(timestamp)d</time>
<timestr>%(timestr)s</timestr>
<command><![CDATA[%(command)s]]></command>
<path>%(path)s</path>
<time_interval>%(time_interval).2f</time_interval>
%(extra)s
</job>
'''
	return xml % {
	    'type':self.type(),
	    'success':self.success,
	    'subject':self.subject,
	    'timestamp' : self.timestamp,
	    'timestr' : self.timestr,
	    'time_interval' : self.time_interval,
	    'path' : self.path,
	    'command' : self.command,
	    'extra': self.extrafields() }
    
class InteractiveRunData(AbstractRunData):
    """Holds data associated with an interactive run"""
    def __init__(self,starttime,endtime,subject,command,success,path):
        AbstractRunData.__init__(self,
                                 starttime=starttime,
                                 endtime=endtime,
                                 subject=subject,
                                 command=command,
                                 success=success,
                                 path=path)

    def type(self):
        return "interactive"

    def extrafields(self):
        return ""



class BatchRunData(AbstractRunData):
    """Holds data associated with a batch run"""
    def __init__(self,starttime,endtime,script,subject,command,success,path):
        AbstractRunData.__init__(self,
                                 starttime=starttime,
                                 endtime=endtime,
                                 subject=subject,
                                 command=command,
                                 success=success,
                                 path=path)
        self.script = script
        self.encoding = platform_specific.encoding # 'base64', 'quopri' or 'raw'

    def type(self):
        return "batch"

    def extrafields(self):
        return '<script encode="%s"><![CDATA[%s]]></script>' % (self.encoding, encode(self.script, self.encoding))

class ProfileRunData(AbstractRunData):
    """Holds data associated with a profiled run"""
    def __init__(self,starttime,endtime,subject,command,success,path,profiledata):
        AbstractRunData.__init__(self,
                                 starttime=starttime,
                                 endtime=endtime,
                                 subject=subject,
                                 command=command,
                                 success=success,
                                 path=path)

        self.profiledata = profiledata

    def type(self):
        return "profiled"

    def extrafields(self):
        return ''.join(["<profiledata><![CDATA[",self.profiledata,"]]></profiledata>"])


class ProfilerReporterData:
    def __init__(self,
                 starttime,
                 endtime,
                 subject,
                 command,
                 success,
                 path,
                 reportdata):
        self.timestamp = starttime
        self.timestr = time.ctime(self.timestamp)
        self.subject = subject
        self.command = command
        self.path = path
        self.time_interval = endtime-starttime
        self.reportdata = reportdata

    def toxml(self):
        return """<profile_report>
<subject>%(subject)s</subject>
<time>%(timestamp)d</time>
<timestr>%(timestr)s</timestr>
<command><![CDATA[%(command)s]]></command>
<path>%(path)s</path>
<time_interval>%(time_interval).2f</time_interval>
<contents><![CDATA[%(reportdata)s]]></contents>
</profile_report>""" % {'subject':self.subject,
                        'timestamp': self.timestamp,
                        'timestr' : self.timestr,
                        'command' : self.command,
                        'path' : self.path,
                        'time_interval' : self.time_interval,
                        'reportdata':self.reportdata}

class DebuggerData:
    """Data associated with the invocation of a debugger"""
    def __init__(self,starttime,endtime,subject,command,success,path):
        self.timestamp = starttime
        self.timestr = time.ctime(self.timestamp)
        self.subject = subject
        self.command = command
        self.success = success
        self.path = path
        self.time_interval = endtime-starttime

    def toxml(self):
        return """<debug success='%(success)d'>
<subject>%(subject)s</subject>
<time>%(timestamp)d</time>
<timestr>%(timestr)s</timestr>
<command><![CDATA[%(command)s]]></command>
<path>%(path)s</path>
<time_interval>%(time_interval).2f</time_interval>
</debug>""" % {
            'success':self.success,
            'subject':self.subject,
            'timestamp': self.timestamp,
            'timestr' : self.timestr,
            'command' : self.command,
            'time_interval' : self.time_interval,
            'path' : self.path}
               

class MakeData:
    def __init__(self,starttime,endtime,subject,command,success,path):
	pass
    
    def toxml(self):
	return "<make></make>"
    
if __name__=='__main__':
    compiler = '/usr/bin/gcc'
    #capture_compile(compiler,platform_specific.logfiledir)
    capture_compile(compiler)
