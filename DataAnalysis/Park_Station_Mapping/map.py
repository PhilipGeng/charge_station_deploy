# _*_ coding:utf-8 _*_

import os

from Park_Station_Mapping.distance import haversine
from Park_Station_Mapping.str_matching import matching_address

from dbapi import dbShell as db
from local_path import BASE_DIR


park_db = db(os.path.join(BASE_DIR, 'db/SHParking.db'))

station_db = db(os.path.join(BASE_DIR, 'db/EVcharge.db'))

park_matrix = park_db.select(table='parkMatrix')
park_dataWash = park_db.select(table='data_wash')
park_dataWash = [e[0] for e in park_dataWash]

park_location = park_db.select(table='ParkBaiduGPS')

station_matrix = station_db.select(table='stationMatrix')

station_location = station_db.select(table='stationBaiduGPS')

parkNearest = {}
stationNearest = {}

threshold = 300
c = 0
for park in park_location:
    c += 1
    print(c)
    ####################################################################################################
    # 外循环遍历park
    ####################################################################################################
    parkID = park[0]
    parkLat = float(park[1])
    parkLng = float(park[2])

    if parkID not in parkNearest:
        parkNearest[parkID] = [None, None, None]
    ####################################################################################################
    # 内循环遍历station
    ####################################################################################################
    for station in station_location:
        stid = station[1]
        opid = station[0]
        stationLat = float(station[2])
        stationLng = float(station[3])

        if stid+opid not in stationNearest:
            stationNearest[stid+opid] = [None, None]

        park_station_dis = haversine(parkLng, parkLat, stationLng, stationLat)
        if None in parkNearest[parkID] or park_station_dis < float(parkNearest[parkID][0]):
            parkNearest[parkID][0] = str(park_station_dis)
            parkNearest[parkID][1] = stid
            parkNearest[parkID][2] = opid

        if None in stationNearest[stid+opid] or park_station_dis < float(stationNearest[stid+opid][0]):
            stationNearest[stid + opid][0] = str(park_station_dis)
            stationNearest[stid + opid][1] = parkID
####################################################################################################
# 对比 park 和 station 的 nearest point, 一对一映射
####################################################################################################
oto_match_counter = 0
oto_match_list = {}
for parkID in parkNearest:
        stid = parkNearest[parkID][1]
        opid = parkNearest[parkID][2]
        if stid+opid in stationNearest and stationNearest[stid+opid][1] == parkID:
            oto_match_counter += 1
            oto_match_list[parkID] = (stid, opid, parkNearest[parkID][0])
# print(oto_match_counter)
####################################################################################################
# 每个park map一个充电站 one to mang
# threshold = 200
####################################################################################################
def one_to_many_saveAll():
    for parkID in parkNearest:
        parkLocation = park_db.select(table='ParkBaiduGPS',
                                      cols='lat,lng',
                                      condition='parkID="%s"' % parkID)
        for location in parkLocation:
            parkLat = float(location[0])
            parkLng = float(location[1])

        park_inf = park_db.select(table='parkMatrix', condition='parkID="%s"' % parkID)
        park_total_num = park_inf[0][2]
        park_calss = park_inf[0][3]
        park_occ = list(park_inf[0][4:52])
        insert_value = [parkID, park_total_num, park_calss, parkLat, parkLng]
        for tmpocc in park_occ:
            insert_value.append(tmpocc)
        if float(parkNearest[parkID][0]) < threshold:
            # park_db.insert(table='ParkBaiduToShow', value=[(parkID, parkLat, parkLng)])
            stid = parkNearest[parkID][1]
            opid = parkNearest[parkID][2]
            station_inf = station_db.select(table='stationMatrix', condition="stid='%s' and opid='%s'" % (stid, opid))
            try:
                station_total_num = station_inf[0][3]
                station_occ = station_inf[0][4:52]
            except Exception as e:
                station_total_num = ''
                station_occ = ''
                print(station_inf)
                print(e)
            insert_value.append(stid)
            insert_value.append(opid)
            insert_value.append(station_total_num)
            for tmpocc in station_occ:
                insert_value.append(tmpocc)
        else:
            for i in range(0, 51):
                insert_value.append('')
        station_db.insert(table='map', value=[tuple(insert_value)])
    pass
####################################################################################################
# 相互最近, 一对一映射, 保存所有
# threshold = 200
####################################################################################################
def one_to_one_saveAll():
    for parkID in parkNearest:
        parkLocation = park_db.select(table='ParkBaiduGPS',
                                      cols='lat,lng',
                                      condition='parkID="%s"' % parkID)
        for location in parkLocation:
            parkLat = float(location[0])
            parkLng = float(location[1])

        park_inf = park_db.select(table='parkMatrix', condition='parkID="%s"' % parkID)
        park_total_num = park_inf[0][2]
        park_calss = park_inf[0][3]
        park_occ = list(park_inf[0][4:52])
        insert_value = [parkID, park_total_num, park_calss, parkLat, parkLng]
        for tmpocc in park_occ:
            insert_value.append(tmpocc)
        if parkID in oto_match_list and float(oto_match_list[parkID][2]) < threshold:
            # park_db.insert(table='ParkBaiduToShow', value=[(parkID, parkLat, parkLng)])
            stid = oto_match_list[parkID][0]
            opid = oto_match_list[parkID][1]
            station_inf = station_db.select(table='stationMatrix', condition="stid='%s' and opid='%s'" % (stid, opid))
            try:
                station_total_num = station_inf[0][3]
                station_occ = station_inf[0][4:52]
            except Exception as e:
                station_total_num = ''
                station_occ = ''
                print(station_inf)
                print(e)
            insert_value.append(stid)
            insert_value.append(opid)
            insert_value.append(station_total_num)
            for tmpocc in station_occ:
                insert_value.append(tmpocc)
        else:
            for i in range(0, 51):
                insert_value.append('')
        station_db.insert(table='map', value=[tuple(insert_value)])
        print(insert_value)
    pass
####################################################################################################
# 相互最近, 一对一映射, 保存所有
# threshold = 200
####################################################################################################
def one_to_one_saveMap():
    map_db = db(os.path.join(BASE_DIR, 'db/map.db'))
    for key in oto_match_list:
        parkID = key
        stid = oto_match_list[parkID][0]
        opid = oto_match_list[parkID][1]
        distance = float(oto_match_list[parkID][2])
        if distance < threshold:
            parkInfos = park_db.select(table='ParkStaticData', cols='parkName,address,parkType,companyName',
                                      condition="parkID='%s'" % parkID)
            parkLocation = park_db.select(table='ParkBaiduGPS',
                                          cols='lat,lng',
                                          condition='parkID="%s"' % parkID)
            for location in parkLocation:
                parkLat = float(location[0])
                parkLng = float(location[1])
            for parkInfo in parkInfos:
                parkName = parkInfo[0]
                parkAddress = parkInfo[1]
                parkType = parkInfo[2]
                parkCompanyName = parkInfo[3]

            stationInfos = station_db.select(table='station_pub', cols='stname,address,constructDesc',
                                             condition="stid='%s' and opid='%s'" % (stid, opid))
            stationLocation = station_db.select(table='stationBaiduGPS',
                                          cols='lat,lng',
                                          condition="stid='%s' and opid='%s'" % (stid, opid))
            for location in stationLocation:
                stationLat = float(location[0])
                stationLng = float(location[1])
            for stationInfo in stationInfos:
                stationName = stationInfo[0]
                stationAddress = stationInfo[1]
                stationConstruct = stationInfo[2]
            insert_value = [(parkID, stid, opid, distance, parkName,
                             stationName, parkAddress, stationAddress,
                             parkCompanyName, stationConstruct,
                             parkLat, parkLng, stationLat, stationLng)]
            map_db.insert(table='map', value=insert_value)

done_station2 = []
done_station1 = []
def insert_once(map_db, parkID, stid, opid, distance, counter, feature):
    parkInfos = park_db.select(table='ParkStaticData', cols='parkName,address,parkType,companyName',
                               condition="parkID='%s'" % parkID)
    parkLocation = park_db.select(table='ParkBaiduGPS',
                                  cols='lat,lng',
                                  condition='parkID="%s"' % parkID)
    for location in parkLocation:
        parkLat = float(location[0])
        parkLng = float(location[1])
    for parkInfo in parkInfos:
        parkName = parkInfo[0]
        parkAddress = parkInfo[1]
        parkType = parkInfo[2]
        parkCompanyName = parkInfo[3]

    stationInfos = station_db.select(table='station_pub', cols='stname,address,constructDesc',
                                     condition="stid='%s' and opid='%s'" % (stid, opid))
    stationLocation = station_db.select(table='stationBaiduGPS',
                                        cols='lat,lng',
                                        condition="stid='%s' and opid='%s'" % (stid, opid))
    for location in stationLocation:
        stationLat = float(location[0])
        stationLng = float(location[1])
    for stationInfo in stationInfos:
        stationName = stationInfo[0]
        stationAddress = stationInfo[1]
        stationConstruct = stationInfo[2]
    match_result = matching_address(parkName, stationName,
                                               parkAddress, stationAddress, distance)
    insert_table = 'map_%s' % match_result
    insert_flag = True
    if match_result == 2:
        if (stid, opid) not in done_station2:
            done_station2.append((stid, opid))
    if match_result == 1 or match_result == 0:
        if (stid, opid) in done_station2:
            insert_flag = False
    if insert_flag:
        insert_value = [(counter, parkID, stid, opid, feature, distance, parkName,
                         stationName, parkAddress, stationAddress,
                         parkCompanyName, stationConstruct,
                         parkLat, parkLng, stationLat, stationLng)]
        map_db.insert(table=insert_table, value=insert_value)


def accuracy(park_address, station_address):
    return 1 if matching_address(park_address, station_address) else -1


def get_feature_value(park_id):
    park_matlab_id = park_db.select(table='parkMatrix', cols='matlabID',
                                    condition="parkID='%s'" % park_id)
    if park_matlab_id.__len__() is 0:
        return 0
    if park_matlab_id[0][0] in park_dataWash:
        return 1
    else:
        return 0


def one_to_many_saveMap():
    map_db = db(os.path.join(BASE_DIR, 'db/map.db'))
    counter = 0
    done = []
    for key in parkNearest:
        parkID = key
        stid = parkNearest[parkID][1]
        opid = parkNearest[parkID][2]
        distance = float(parkNearest[parkID][0])
        if distance < threshold and parkID not in done:
            counter += 1
            insert_once(map_db, parkID, stid, opid, distance, counter, get_feature_value(parkID))
            done.append(parkID)
            for i in parkNearest:
                if stid == parkNearest[i][1] and opid == parkNearest[i][2] and \
                                float(parkNearest[i][0]) < threshold and i not in done:
                    counter += 1
                    insert_once(map_db, i, parkNearest[i][1], parkNearest[i][2], parkNearest[i][0], counter,
                                get_feature_value(i))
                    done.append(i)
    map_db.close()


def clear_data():
    map_db = db(os.path.join(BASE_DIR, 'db/map.db'))
    map_0 = map_db.select(table='map_0', cols='parkID,stid,opid')
    for record in map_0:
        parkID = record[0]
        stid = record[1]
        opid = record[2]
        test2 = map_db.select(table='map_2', condition="stid='%s' and opid='%s'" % (stid, opid))
        test1 = map_db.select(table='map_1', condition="stid='%s' and opid='%s'" % (stid, opid))
        if test1.__len__() is not 0 or test2.__len__() is not 0:
            map_db.delete(table='map_0', condition="parkID='%s'" % parkID)
    map_db.close()

if __name__ == '__main__':
    one_to_many_saveMap()
    clear_data()
    # map_0 unsure: pt31010700042 zb31010800238
