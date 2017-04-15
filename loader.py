from checker import *
from resultDealer import *
import socket
import datetime

path = 'D:\\PaperW\\Stage2\\droidData\\test\\'
now = datetime.datetime.now()
now.strftime('%Y-%m-%d')
# print str(now)[:10]
hostname = socket.gethostname()
sep = os.path.sep
if not os.path.exists(path + "out"):
    os.mkdir(path + "out")
result = os.listdir(path)
for name in result:
    dir = path + name + sep
    if not os.path.exists(dir):
        print "directory or file: " + dir + "not exists"
        continue
    print dir
    result1 = check(dir)
deal(path + 'out' + sep, path + 'out' + sep + hostname + '-' + str(now)[:10] + '.xls')
