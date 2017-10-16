import os
import numpy as np
import sqlite3
import math
import time
from saveMethod import save_txt
from base_dir import dbPath

writebase = './'
dbname = 'EVs.db'
try:
    os.mkdir(writebase+'evstop')
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

dataT = np.zeros((2,24,latgridnum,lnggridnum))
print(dataT.shape)

conn = sqlite3.connect(dbPath+dbname)
c = conn.cursor()
sql1 = "select time,hour,baidulat,baidulng,duration from evstop"

cursor = c.execute(sql1)
cnt = 0
err = 0
for row in cursor:
    cnt += 1
    date = row[0].split(" ")[0]
    weekday = 0 if(time.strptime(date,"%Y-%m-%d").tm_wday<5) else 1
    hour = int(row[1])
    lng = float(row[3])
    lat = float(row[2])
    duration = (float(row[4])/3600)
    lngidx = math.floor((lng-left)/lngperkm)
    latidx = latgridnum - math.floor((lat-bottom)/latperkm) - 1
    d = -1
    while(d<duration):
        d+=1
        try:
            dataT[weekday][(d+hour)%24][latidx][lngidx] += 1
        except Exception:
            err += 1
            print(row)
print(cnt)
print(err)
for i in [0,1]:
    data = dataT[i]
    if(i==1):
        day = "holiday"
    else:
        day = "workday"
    c = -1
    for mat in data:
        c+=1
        summation = int(np.sum(mat))
        fname = writebase+"evstop/"+str(c)+"_"+day+"_"+str(summation)+'.txt'
        # save_txt(mat, fname)
        np.savetxt(fname,mat.transpose(),fmt='%i',delimiter=',')

    s1 = np.sum(data[6:10],axis=0)
    s2 = np.sum(data[10:16],axis=0)
    s3 = np.sum(data[16:22],axis=0)
    s4 = np.sum(data[22:24],axis=0)+np.sum(data[0:6],axis=0)
    slist = [s1,s2,s3,s4]
    for i in range(0,len(slist)):
        c='s'+str(i+1)
        summation = int(np.sum(slist[i]))
        mat = slist[i]
#        fname = writebase + "evstop/" + str(c) + "_" + day + "_" + str(summation) + '.txt'
#        np.savetxt(fname,mat.transpose(),fmt='%i',delimiter=',',newline=';')
        normmat = mat/(1.0*np.max(mat))
        fname = writebase + "evstop/" + str(c) + "_" + day + ".txt"
        fname2 = "aggregate/evstop_" + str(c) + "_" + day + ".txt"
        # np.savetxt(fname,normmat.transpose(),fmt='%f',delimiter=',',newline=';')
        np.savetxt(fname2,normmat.transpose(),fmt='%f',delimiter=',')
        # save_txt(normmat, fname)
        # save_txt(normmat, fname2)


