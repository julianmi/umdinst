#!/usr/bin/env python
#
# A pure Python replacement for wget --post-file


import httplib
import urlparse
import getopt
import sys

default_file=''
default_host='localhost'
default_metadata=None
default_path='/'
default_protocol='http'

class Uploader:
    # Constructor

    def __init__(self):
        self.file = default_file
        self.host = default_host
        self.metadata = default_metadata
        self.path = default_path
        self.protocol = default_protocol

    # Getters/setters

    def getFile(self):
        return self.file

    def setFile(self, file):
        self.file = file or ''

    def getHost(self):
        return self.host

    def setHost(self, host):
        self.host = host or ''

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path or ''

    def getProtocol(self):
        return self.protocol

    def setProtocol(self, protocol):
        self.protocol = protocol or ''

    # Upload

    def upload(self):
        if (self.protocol == 'http'):
            return self.uploadHttp()
#        elsif (self.protocol == 'https'):
#            return self.uploadHttps()
        else:
            return None

    def encodeFile(self):
        boundary = '-----------------------------7717h869P1445c5887S88940647%s\r\n'
        metadataheader = 'Content-Disposition: form-data; name="%s"\r\n\r\n'
        contentheader = 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n\r\n'
        crlf = '\r\n'
        return (boundary % '') + (metadataheader % 'metadata') + self.metadata + crlf + (boundary % '') + (contentheader % ('file', self.file)) + open(self.file, 'rb').read() + crlf + (boundary % '--')

    def uploadHttp(self):
        try:
            httpConnection = httplib.HTTPConnection(self.host)
            headers = {
                'User-Agent': 'backup.py',
                'Accept': '*/*',
                'Accept-Encoding': '*',
                'Content-Type': 'application/octet-stream'
                }
            if self.metadata:
                data = self.encodeFile()
            else:
                data = open(self.file, 'rb').read()
            httpConnection.request('POST', self.path, data, headers)
            response = httpConnection.getresponse()
            if response.status != 200:
                print 'Error:', response.status, response.reason
                return ''
            return response.read()
        except IOError:
            print 'File cannot be read: ' + self.file
            return ''

# Usage
def usage():
    print 'upload.py [--metadata=string] --post-file=file url'

# Main
def main():
    try:
        uploader = Uploader()
        optlist, args = getopt.getopt(sys.argv[1:], 'h', ['help', 'post-file=', 'metadata='])
        for opt in optlist:
            if (opt[0] == '-h' or opt[0] == '--help'):
                usage()
                sys.exit(0)
            elif (opt[0] == '--post-file'):
                uploader.setFile(opt[1])
            elif (opt[0] == '--metadata'):
                uploader.metadata = opt[1]
            else: # this should not happen
                usage()
                sys.exit(-1)
        if (len(args) != 1):
            usage()
            sys.exit(-1)
        (scheme, netloc, path, parameters, query, fragment) = urlparse.urlparse(args[0])
        uploader.setProtocol(scheme)
        uploader.setHost(netloc)
        if parameters:
            path = path + ';' + parameters
        if query:
            path = path + '?' + query
        if fragment:
            path = path + '#' + fragment
        uploader.setPath(path)
        print uploader.upload()
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

        
if __name__ == "__main__":
    main()
