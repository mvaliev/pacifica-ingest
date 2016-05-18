import pycurl
from StringIO import StringIO
import os


bundle_path = "baby.tar"

print "file size: " + str(os.path.getsize(bundle_path))

c = pycurl.Curl()

c.setopt(c.URL, "http://127.0.0.1:8066/upload")
#c.setopt(c.URL, "http://127.0.0.1/upload")

#####
c.setopt(c.HTTPHEADER, ['Content-Type: application/octet-stream'])
c.setopt(pycurl.POSTFIELDSIZE_LARGE, os.path.getsize(bundle_path))
c.setopt(c.POST, 1)
fin = open(bundle_path,'rb')
c.setopt(c.READFUNCTION, fin.read)

#####

odata = StringIO()
c.setopt(pycurl.WRITEFUNCTION, odata.write)

c.setopt(c.VERBOSE, 1)

c.perform()
c.close()

result = odata.getvalue()

print result