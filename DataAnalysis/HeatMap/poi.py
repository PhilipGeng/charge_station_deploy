import os
import numpy as np
import sqlite3
import math
from base_dir import dbPath
from saveMethod import save_txt

writebase = './'
dbname = 'poi2.db'
try:
    os.mkdir(writebase+'poi')
except Exception:
    pass


lngperkm = 0.009
latperkm = 0.0103
bottom = 30.408258525468
top = 32.408258525468
left = 120.22177414094
right = 122.22177414094
latgridnum = int((top-bottom)/latperkm)
lnggridnum = int((right-left)/lngperkm)

dataT = np.zeros((latgridnum,lnggridnum))
print(dataT.shape)

conn = sqlite3.connect(dbPath+dbname)
c = conn.cursor()
sql1 = "select baidulat,baidulng from poi"

cursor = c.execute(sql1)
cnt = 0
err = 0
for row in cursor:
    cnt += 1
    lng = float(row[1])
    lat = float(row[0])
    lngidx = math.floor((lng-left)/lngperkm)
    latidx = latgridnum - math.floor((lat-bottom)/latperkm) - 1
    try:
        dataT[latidx][lngidx] += 1
    except Exception:
        err += 1
        print(row)

summation = int(np.sum(dataT))
print(summation)
fname = writebase+"poi/allpoi_"+str(summation)+'.txt'
# np.savetxt(fname,dataT.transpose(),fmt='%f',delimiter=',',newline=';')
# save_txt(dataT, fname)

normmat = dataT / (1.0 * np.max(dataT))
fname = writebase+"poi/allpoi.txt"
fname2 = writebase+"aggregate/poi.txt"
# save_txt(normmat, fname)
# save_txt(normmat, fname2)
# np.savetxt(fname, normmat.transpose(), fmt='%f', delimiter=',', newline=';')
np.savetxt("aggregate/poi.txt", normmat.transpose(), fmt='%f', delimiter=',')

