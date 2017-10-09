# _*_  coding:utf-8 _*_

import os

from Park_Station_Mapping.distance import haversine

# def haversine(lon1, lat1, lon2, lat2):
from dbapi import dbShell as db


def mapping(SHParking, Stations, threshold):
    parksID = SHParking.select(table='parkMatrix', cols='parkID')
    stations = Stations.select(table='station', cols='stid,lat,lng')
    for parkID in parksID:
        park_location = SHParking.select(table='ParkStaticData', cols='entLati,entLongi',
                                    condition='parkID="%s"' % parkID[0])
        if park_location.__len__() == 0:
            park_location = SHParking.select(table='Park', cols='entLati,entLongi',
                                             condition='parkID="%s"' % parkID[0])
        park_lat = float(park_location[0][0])
        park_lon = float(park_location[0][1])
        nearby = ''
        nearbyNum = 0
        for station in stations:
            stationID = station[0]
            station_lat = float(station[1])
            station_lon = float(station[2])
            distance = haversine(park_lon, park_lat, station_lon, station_lat)
            if distance < threshold:
                nearby += '%s:%f;' % (stationID, distance)
                nearbyNum += 1
        if nearby:
            SHParking.insert(table='mappingParkStation', value=[(parkID[0], threshold, nearbyNum, nearby)])
            print([(parkID[0], threshold, nearbyNum, nearby)])
    pass


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SHParking = db(os.path.join(BASE_DIR, 'db/SHParking.db'))

    Stations = db(os.path.join(BASE_DIR, 'db/EVcharge.db'))

    threshold = 200  # 米

    mapping(SHParking, Stations, threshold)