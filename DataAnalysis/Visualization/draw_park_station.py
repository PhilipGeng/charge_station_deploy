# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from dbapi import dbShell as db
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    Parks = db(os.path.join(BASE_DIR, 'db/SHParking.db'))
    Stations = db(os.path.join(BASE_DIR, 'db/EVcharge.db'))

    station_locations = Stations.select(table='stationBaiduGPS',
                                        cols='lat,lng')
    station_x = []
    station_y = []
    for station_location in station_locations:
        station_x.append(station_location[0])
        station_y.append(station_location[1])

    park_locations = Parks.select(table='ParkBaiduToShow',cols='lat,lng')
    park_x = []
    park_y = []
    for park_location in park_locations:
        park_x.append(park_location[0])
        park_y.append(park_location[1])

    # plt.figure(1, figsize=(20, 10))
    one = False
    if one:
        plt.scatter(station_x, station_y, c='green', s=20, label='station', alpha=1, edgecolors='white')
        plt.scatter(park_x, park_y, c='red', s=20, label='parks', alpha=0.5, edgecolors='white')
        plt.title('Parks & Stations')
        plt.xlabel('lat')
        plt.ylabel('long')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        p1 = plt.subplot(2,1,1)
        p2 = plt.subplot(2,1,2)
        p1.scatter(station_x, station_y, c='green', s=20, label='station', alpha=1, edgecolors='white')
        p2.scatter(park_x, park_y, c='red', s=20, label='parks', alpha=0.5, edgecolors='white')
        plt.title('Parks & Stations')
        plt.xlabel('lat')
        plt.ylabel('long')
        p1.legend()
        p2.legend()
        plt.grid(True)
        plt.show()
    pass