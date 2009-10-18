#!/usr/bin/env python
#
# Back up the data to the server
import getopt
import shutil
import md5
import os
import sys
import string
import zipfile
import socket

try:
    import configlocal
except ImportError:
    print "Error: configlocal.py not found"
    print "Run setup.py to generate configlocal.py file"
    sys.exit(1)

# Fix for older versions of Python
try:
    True
except NameError:
    True,False = 1,0


# Not all systems have _socket
# If not, we fall back on using wget
try:
    import upload
    uploadSupported = True
except ImportError:
    uploadSupported = False

default_file=''
default_host='localhost'
default_path='/'
default_protocol='http'

class Backup:
   def __init__(self,uploadSupported):
       self.datadir = ''
       self.host = ''
       self.listFile = ''
       self.manifestFile = ''
       self.timestampFile = ''
       self.zipFile = ''
       self.host = default_host
       self.path = default_path
       self.protocol = default_protocol
       self.forceAll = False
       self.quiet = False
       self.uploadSupported = uploadSupported

   def printMessage(self, message):
       if not self.quiet:
           print message,
           sys.stdout.flush()

   # Check if the given file name exists and it's a regular file
   # (Meant to be equivalent to [ -f file ] in shell script)
   def isRegularFile(self, file):
#        try:
#            stat_manifest = os.stat(file)
#            return stat.S_ISREG(stat_manifest[stat.ST_MODE])
#        except OSError:
#            return False
       return os.path.isfile(file)

   def filesize(self, file):
       if self.isRegularFile(file):
#            stat_manifest = os.stat(file)
#            return stat_manifest[stat.ST_SIZE]
           return os.path.getsize(file)
       else:
           return 0

   def md5sum(self, file):
       if self.isRegularFile(file):
           m = md5.new()
           m.update(open(file, 'rb').read())
           return m.hexdigest()
       else:
           return None

   def do_archive(self):
       self.printMessage('Creating an archive file... ')
       # Check if the timestamp from previous update should be used
       if (not self.forceAll) and self.isRegularFile(self.timestampFile):
           # Find file newer than the timestamp
           baseTimestamp = os.path.getmtime(self.timestampFile)
       else:
           # Find all files
           baseTimestamp = 0
       # Create a new zip file
       zipFile = zipfile.ZipFile(self.zipFile, 'w')
       fileListFile = open(self.listFile, 'w')
       fileList = [os.path.join(self.dataDir,f)
		   for f in os.listdir(self.dataDir)
		   if (f.endswith('.log') or f.endswith('.hist')) and
		   os.path.getmtime(os.path.join(self.dataDir,f)) > baseTimestamp]
       for logfile in fileList:
           zipFile.write(logfile)
           fileListFile.write(logfile)
       fileListFile.close()
       zipFile.write(self.listFile)
       zipFile.write(self.manifestFile)
       zipFile.close()
       self.printMessage('done\n')


   def do_upload(self):
       """Upload the data."""
       self.printMessage('Uploading logfile... ')
       if self.uploadSupported:
           return self._do_upload()
       else:
           return self._do_upload_with_wget()
       self.printMessage('done\n')

   def _do_upload(self):
       """Upload the data using the Python uploader"""
       uploader = upload.Uploader()
       uploader.setProtocol(self.protocol)
       uploader.host = self.host
       uploader.path = self.path
       uploader.setFile(self.zipFile)
       response = uploader.upload()
       return response

   def _do_upload_with_wget(self):
       """Upload the data using wget"""
       cmd = "wget -q -O - --post-file=%s %s://%s%s" % (self.zipFile,
                                                       self.protocol,
                                                       self.host,
                                                       self.path)
       (stdin,stdouterr) = os.popen4(cmd)
       response = stdouterr.read()
       return response
       

   def do_verify(self, response):
       self.printMessage('Verifying... ')
       if (len(response) == 0):
           print 'Server returned an empty response. Upload failed.'
           sys.exit(-1)
       [ressize, resmd5] = string.split(response)
       size = self.filesize(self.zipFile)
       if str(ressize) != str(size):
           print 'File size does not match. Upload failed.'
           sys.exit(-1)
       md5val = self.md5sum(self.zipFile)
       if resmd5 != md5val:
           print 'MD5 checksum do not match. Upload failed.'
           sys.exit(-1)
       self.printMessage('done\n')

   def execute(self):
       # Make sure that the manifest file exists
       if not self.isRegularFile(self.manifestFile):
           print 'Manifest file %s not found' % self.manifestFile
           sys.exit(-1)
       # Create the zip archive file
       self.do_archive()
       # Upload the file
       response = self.do_upload()
       # Verify the server response
       self.do_verify(response)
       # Update timestamp file
       # This only happens when the file upload is successful
       # The timestamp file should be update so that it has the
       # timestamp idential to the zip archive file.
       # (Notice that the log file may have been updated during uploading)

       # Get the time from the zipfile
       timestamp = os.path.getmtime(self.zipFile)

       # Create an empty timestamp file
       open(self.timestampFile,'w').close()

       # Set the access time
       os.utime(self.timestampFile,(timestamp,timestamp))
       

   # Create manifest file- tentative implementation
   def createManifestFile(self):
       f = open(self.manifestFile, 'w')
       f.write("classid=%s\n" % configlocal.vars['classid'])
       f.write("hostname=%s\n" % socket.gethostname())
       f.close()

# Display usage
def usage():
   str = """Usage: %s [OPTION]
Upload the log file archive to the server

 -f   force all log files to be uploaded
 -h   display this help and exit
 -M   create a manifest file
 -q   quiet mode: turn off most output

"""
   print str % sys.argv[0]


# Main
def main():
   try:
       # Set default parameters
       backup = Backup(uploadSupported)
       prefix = os.path.dirname(sys.argv[0])
       backup.dataDir = configlocal.vars['logfiledir']
       backup.manifestFile = os.path.join(backup.dataDir, "00manifest")
       backup.timestampFile = os.path.join(backup.dataDir,"00timestamp")
       backup.listFile = os.path.join(backup.dataDir, "00files")
       backup.zipFile = os.path.join(backup.dataDir, "00upload.zip")

       backup.protocol = 'http'
       backup.host = configlocal.vars['upload_host']
       backup.path = configlocal.vars['upload_path']
       # Process command-line arguments
       optlist, args = getopt.getopt(sys.argv[1:], 'fhMq', ['help'])
       for opt in optlist:
           if (opt[0] == '-h' or opt[0] == '--help'):
               usage()
               sys.exit(0)
           elif (opt[0] == '-f'):
               backup.forceAll = True
           elif (opt[0] == '-M'):
               backup.createManifestFile()
               sys.exit(0)
           elif (opt[0] == '-q'):
               backup.quiet = True
           else: # this should not happen
               usage()
               sys.exit(-1)
       if (len(args) != 0):
           usage()
           sys.exit(-1)
       # Run the main process
       backup.execute()
   except getopt.GetoptError:
       usage()
       sys.exit(-1)


if __name__ == "__main__":
   main()
