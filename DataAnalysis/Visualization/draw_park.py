# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from dbapi import dbShell as db
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

park_db = db(os.path.join(BASE_DIR, 'db/SHParking.db'))

station_db = db(os.path.join(BASE_DIR, 'db/EVcharge.db'))

park_matrix = park_db.select(table='parkMatrix')
park_dataWash = park_db.select(table='data_wash')
park_dataWash = [e[0] for e in park_dataWash]


def normalize(park_occ):
    max_occ = max(park_occ)
    min_occ = min(park_occ)
    park_occ = [((e - min_occ) / (max_occ - min_occ)) for e in park_occ]
    return park_occ


for park in park_matrix:
    ####################################################################################################
    # 遍历park
    ####################################################################################################
    # wash data
    matlabID = park[1]
    if matlabID not in park_dataWash:
        continue
    parkID = park[0]
    totalNum = park[2]
    parkClass = park[3]
    park_occ = np.array(normalize([float(e) for e in park[4:52]]))
    hour = np.array(range(0, 48))

    plt.figure(1, figsize=(20, 10))
    axes = plt.subplot(111)
    plt.plot(hour, park_occ, 'bo', hour, park_occ, 'k')
    plt.xlabel('hour')
    plt.ylabel('occupancy')
    axes.set_yticks([e / 20.0 for e in range(0, 21)])
    axes.set_xticks([e for e in range(0, 48)])
    plt.title('parkID = %s, totalNum = %s' % (parkID, totalNum))
    plt.grid(True)
    axis_font = {'fontname': 'Arial', 'size': '10'}
    # plt.show()
    plt.savefig('/Users/chaidi/Documents/RA-Documents/ParkingDataVis/%s.png' % (parkID))
    print('File saved in ParkingDataVis/%s.png' % (parkID))
    plt.close()