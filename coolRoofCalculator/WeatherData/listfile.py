import os
from os import listdir

from os.path import isfile, join
mypath = os.path.dirname(os.path.abspath(__file__))
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.sort(reverse=False)
print onlyfiles
length = len(onlyfiles)
f = open('listOfWeatherFiles.txt','w')
for i in range(length):
	f.write(onlyfiles[i])
	f.write('\n')
f.close()

