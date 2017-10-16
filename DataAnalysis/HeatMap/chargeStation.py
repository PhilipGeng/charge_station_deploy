import os
import numpy as np
import sqlite3
import math
from base_dir import dbPath
from saveMethod import save_txt

var_flag = False

writebase = './'
dbname = 'EVcharge.db'
try:
    os.mkdir(writebase+'chargeStation')
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
sql1 = "select * from stationBaiduGPS"

cursor = c.execute(sql1)
cnt = 0
err = 0
rows = cursor.fetchall()
for row in rows:
    cnt += 1
    lng = float(row[3])
    lat = float(row[2])
    stid = row[1]
    opid = row[0]
    lngidx = math.floor((lng-left)/lngperkm)
    latidx = latgridnum - math.floor((lat-bottom)/latperkm) - 1
    sql1 = "select totalNum from stationMatrix where stid='%s' and opid='%s'" % (stid, opid)
    cursor = c.execute(sql1)
    try:
        totalNum = int(cursor.fetchone()[0])
    except Exception:
        totalNum = 1
        print(stid, opid)
    try:
        dataT[latidx][lngidx] += totalNum
    except Exception:
        err += 1
        print(row)
summation = int(np.sum(dataT))
print(summation)
fname = writebase+"chargeStation/allstation_"+str(summation)+'.txt'
if var_flag:
    save_txt(dataT, fname)
else:
    np.savetxt(fname,dataT.transpose(),fmt='%f',delimiter=',')

    normmat = dataT / (1.0 * np.max(dataT))
    fname = writebase+"chargeStation/allstation.txt"
    fname2 = writebase+"aggregate/allstation.txt"

    # np.savetxt(fname, normmat.transpose(), fmt='%f', delimiter=',')
    np.savetxt(fname2, normmat.transpose(), fmt='%f', delimiter=',')

# normmat = dataT / (1.0 * np.max(dataT))
# fname = writebase+"chargeStation/allstation.txt"
# fname2 = writebase+"aggregate/poi.txt"
# save_txt(normmat, fname)
# save_txt(normmat, fname2)
# np.savetxt(fname, normmat.transpose(), fmt='%f', delimiter=',', newline=';')
# np.savetxt("aggregate/poi.txt", normmat.transpose(), fmt='%f', delimiter=',')

