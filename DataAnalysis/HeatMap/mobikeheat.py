import os
import numpy as np
import sqlite3
import math
import time
from base_dir import dbPath
from saveMethod import save_txt

writebase = './'
dbname = 'mobike.db'
try:
    os.mkdir(writebase+'mobike')
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

'''
dim1: workday/holiday
dim2: 24hours
dim3/4: lat/lng
'''

dataT = np.zeros((2,24,latgridnum,lnggridnum))
print(dataT.shape)

conn = sqlite3.connect(dbPath+dbname)
c = conn.cursor()
sql1 = "select time,baidulng,baidulat from checkin"
sql2 = "select time,baidulng,baidulat from checkout"
cursor = c.execute(sql1)
cnt = 0
err = 0
for row in cursor:
    cnt += 1
    t = row[0]
    date = t.split(" ")[0]
    weekday = 0 if(time.strptime(date,"%Y-%m-%d").tm_wday<5) else 1
    hour = int(t.split(" ")[1].split(":")[0])
    lng = float(row[1])
    lat = float(row[2])
    lngidx = math.floor((lng-left)/lngperkm)
    latidx = latgridnum - math.floor((lat-bottom)/latperkm) - 1
    try:
        dataT[weekday][hour][latidx][lngidx] += 1
    except Exception:
        err += 1
        print(row)
cursor = c.execute(sql2)
for row in cursor:
    cnt += 1
    t = row[0]
    date = t.split(" ")[0]
    weekday = 0 if(time.strptime(date,"%Y-%m-%d").tm_wday<5) else 1
    hour = int(t.split(" ")[1].split(":")[0])
    lng = float(row[1])
    lat = float(row[2])
    lngidx = math.floor((lng-left)/lngperkm)
    latidx = latgridnum - math.floor((lat-bottom)/latperkm) - 1
    try:
        dataT[weekday][hour][latidx][lngidx] += 1
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
        fname = writebase+"mobike/"+str(c)+"_"+day+"_"+str(summation)+'.txt'
        # np.savetxt(fname,mat.transpose(),fmt='%i',delimiter=',')
        # save_txt(mat, fname)
    s1 = np.sum(data[6:10],axis=0)
    s2 = np.sum(data[10:16],axis=0)
    s3 = np.sum(data[16:22],axis=0)
    s4 = np.sum(data[22:24],axis=0)+np.sum(data[0:6],axis=0)
    slist = [s1,s2,s3,s4]
    for i in range(0,len(slist)):
        c='s'+str(i+1)
        mat = slist[i]
        summation = int(np.sum(slist[i]))
#        fname = writebase + "mobike/" + str(c) + "_" + day + "_" + str(summation) + '.txt'
#        np.savetxt(fname,mat.transpose(),fmt='%i',delimiter=',',newline=';')
        normmat = mat/(1.0*np.max(mat))
        # fname = writebase + "mobike/" + str(c) + "_" + day + ".txt"
        # np.savetxt(fname,normmat.transpose(),fmt='%f',delimiter=',')
        # save_txt(normmat, fname)

        fname2 = "aggregate/mobike_" + str(c) + "_" + day + ".txt"
        np.savetxt(fname2,normmat.transpose(),fmt='%f',delimiter=',')
        # save_txt(normmat, fname2)

