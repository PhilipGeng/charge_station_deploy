# _*_ coding:utf-8 _*_
# 代码描述:对地图格子上的
# Input:
# Output:
import os
from dbapi import dbShell as db
import math
from local_path import dbPath as dbpath

EVcharge = db(dbpath + 'EVcharge.db')
poi = db(dbpath + 'poi2.db')
SHParking = db(dbpath + 'SHParking.db')

park_obj_GPSs = SHParking.select(table='ParkBaiduGPSMap')
poi_obj_infs = poi.select(table='poi', cols='baidulat,baidulng,type1,type2,type3')
station_obj_GPSs = EVcharge.select(table='stationBaiduGPS')

lngperkm = 0.009
latperkm = 0.0103
bottom = 30.408258525468
top = 32.408258525468
left = 120.22177414094
right = 122.22177414094
latgridnum = int((top-bottom)/latperkm)
lnggridnum = int((right-left)/lngperkm)

# lng lat
block_location = [[121.486576, 31.239016],
                  [121.450356, 31.227901],
                  [121.522795, 31.238769],
                  [121.440582, 31.249637],
                  [121.477664, 31.228395],
                  # The last two are new boundaries
                  [120.892544, 31.948285],
                  [122.110215, 30.351207]
                  ]

# block_location = []

# park_objs = EVcharge.select(table='map', cols='parkID')
#
# for park_obj in park_objs:
#     parkID = park_obj[0]
#     park_obj_GPS = SHParking.select(table='ParkBaiduGPS', condition="parkID='%s'" % parkID)
#     try:
#         SHParking.insert(table='ParkBaiduGPSMap', value=park_obj_GPS)
#     except Exception:
#         print(parkID, Exception)


park_obj_all = []
poi_obj_all = []
poi_total_num = []
block_all = []
station_total_num = []
for lng, lat in block_location:
    lngidx = math.floor((lng - left) / lngperkm)
    latidx = latgridnum - math.floor((lat-bottom)/latperkm) - 1

    left_border = left + lngidx * lngperkm  # - (threshold - 1) * lngperkm
    right_border = left_border + lngperkm  # + (threshold - 1) * lngperkm
    top_border = top - latidx * latperkm  # + (threshold - 1) * latperkm
    bottom_bodder = top_border - latperkm  # - (threshold - 1) * latperkm
    print('border:')
    print(left_border, right_border, top_border, bottom_bodder)

    block = [left_border, right_border, top_border, bottom_bodder]
    block_all.append(block)
    #############################################################################################
    # 停车场
    #############################################################################################
    park_obj = []

    # 获得格子里所有停车场的匹配数据
    for park_obj_GPS in park_obj_GPSs:
        parkID = park_obj_GPS[0]
        park_lat = float(park_obj_GPS[1])
        park_lng = float(park_obj_GPS[2])
        if park_lat < top_border and park_lat > bottom_bodder and park_lng < right_border and park_lng > left_border:
            try:
                park_obj.append(EVcharge.select(table='map', condition="parkID='%s'" % parkID))
            except Exception:
                print(parkID, Exception)
    # print(park_obj.__len__())
    park_obj_all.append(park_obj)
    ######################################################################################
    # POI
    ######################################################################################
    poi_obj = {}
    poi_counter = 0
    # 获得格子里所有停车场的匹配数据
    for poi_obj_inf in poi_obj_infs:
        poi_lat = float(poi_obj_inf[0])
        poi_lng = float(poi_obj_inf[1])
        type1 = poi_obj_inf[2]
        type2 = poi_obj_inf[3]
        type3 = poi_obj_inf[4]
        final_type = type1
        if poi_lat < top_border and poi_lat > bottom_bodder and poi_lng < right_border and poi_lng > left_border:
            if final_type in poi_obj:
                poi_obj[final_type] += 1
            else:
                poi_obj[final_type] = 1
            poi_counter += 1
    # print(poi_obj.__len__())
    poi_total_num.append(poi_counter)
    poi_obj_all.append(poi_obj)
    #############################################################################################
    # 充电桩
    #############################################################################################
    station_counter = 0
    station_num_tmp = 0
    # 获得格子里所有停车场的匹配数据
    for station_obj_GPS in station_obj_GPSs:
        stid = station_obj_GPS[1]
        opid = station_obj_GPS[0]
        station_lat = float(station_obj_GPS[2])
        station_lng = float(station_obj_GPS[3])
        if station_lat < top_border and station_lat > bottom_bodder and station_lng < right_border and station_lng > left_border:
            try:
                station_info = EVcharge.select(table='stationMatrix',
                                               cols='totalNum',
                                               condition="stid='%s' and opid='%s'" % (stid, opid))
                station_counter += 1
                station_num_tmp += int(station_info[0][0])
            except Exception:
                print(stid, opid, Exception)
    station_total_num.append([station_counter, station_num_tmp])


for i in range(0, block_location.__len__()):
    print("###############################################")
    print('充电站数量: %s 充电桩数量: %s' % (station_total_num[i][0], station_total_num[i][1]))
    print(block_all[i])
    poi_num = poi_total_num[i]
    print(poi_num)
    poi_obj = poi_obj_all[i]
    for key in poi_obj:
        value = poi_obj[key]
        print(key, value, float(value)/float(poi_num))
    park_objs = park_obj_all[i]
    counter = 0
    for park_obj in park_objs:
        parkID = park_obj[0][0]
        totalNum = park_obj[0][1]
        stid = park_obj[0][53]
        location = SHParking.select(table='ParkBaiduGPSMap', cols='lat,lng', condition="parkID='%s'" % parkID)
        park_lat = location[0][0]
        park_lng = location[0][1]
        if stid == '':
            counter += 1
            print('0', parkID, totalNum, '%s,%s' % (park_lng, park_lat))
        else:
            print('1', parkID, totalNum, '%s,%s' % (park_lng, park_lat))
    print("###############################################")

# for park_objs in park_obj_all:
#     counter = 0
#     for park_obj in park_objs:
#         parkID = park_obj[0][0]
#         totalNum = park_obj[0][1]
#         stid = park_obj[0][53]
#         location = SHParking.select(table='ParkBaiduGPSMap', cols='lat,lng', condition="parkID='%s'" % parkID)
#         park_lat = location[0][0]
#         park_lng = location[0][1]
#         if stid == '':
#             counter += 1
#             print('0', parkID, totalNum, '%s,%s' % (park_lng, park_lat))
#         else:
#             print('1', parkID, totalNum, '%s,%s' % (park_lng, park_lat))
#     print("###############################################")
