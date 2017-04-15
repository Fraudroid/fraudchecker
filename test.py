import os

sep = os.path.sep
path = 'I:\\new_out'
pd = os.listdir(path)
for allDir in pd:
    print allDir
    child = path + sep + allDir + sep + 'states'
    print child
