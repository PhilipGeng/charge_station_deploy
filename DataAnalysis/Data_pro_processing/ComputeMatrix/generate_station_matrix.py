from dbapi import dbShell as db
import os
# 2017-06-20 2017-08-21
weekendList = ['2017-06-24', '2017-06-25', '2017-07-01', '2017-07-02',
               '2017-07-08', '2017-07-09', '2017-07-15', '2017-07-16',
               '2017-07-22', '2017-07-23', '2017-07-29', '2017-07-30',
               '2017-08-05', '2017-08-06', '2017-08-12', '2017-08-13',
               '2017-08-19', '2017-08-20']

charge_station = db('/Users/chaidi/Documents/RA-Documents/DataAnalysis/db/EVcharge.db')
stations = charge_station.select(table='stationOcc', orderby='stid,opid')

id_dic = {}
id_dic_counter = 0
station_matrix = []
for station in stations:
    # station sample
    # < class 'tuple'>: ('10007', 'MA1FP0228', '2017-06-20', '13', '0.100', '10')
    stid = str(station[0])
    opid = str(station[1])
    date = station[2]
    hour = station[3]
    occ = float(station[4])
    totalNum = str(station[5])
    # 区分周六日
    if date in weekendList:
        hour = str(24 + int(hour))
    if stid + opid not in id_dic:
        id_dic[stid + opid] = id_dic_counter
        station_matrix.append((stid, opid, id_dic_counter+1, totalNum, {}, {})) # 第一个词典求和，第二个字典计数求平均
        id_dic_counter += 1
    index = id_dic[stid + opid]
    try:
        if hour not in station_matrix[id_dic[stid + opid]][4]:
            station_matrix[index][4][hour] = occ # 第一个词典求和，第二个字典计数求平均
            station_matrix[index][5][hour] = 1
        else:
            station_matrix[index][4][hour] = occ + station_matrix[index][4][hour] # 第一个词典求和，第二个字典计数求平均
            station_matrix[index][5][hour] += 1
    except Exception:
        print(stid + opid)
        print(date, hour)
    pass
for each_station in station_matrix:
    for hour_occ in each_station[4]:
        each_station[4][hour_occ] = each_station[4][hour_occ] / each_station[5][hour_occ]

# save matrix to database
for each_station in station_matrix:
    stid = str(each_station[0])
    opid = str(each_station[1])
    matlabID = str(each_station[2])
    totalNum = str(each_station[3])
    insert_value = [stid, opid, matlabID, totalNum]
    for i in range(0,48):
        hour = '0' + str(i) if i < 10 else str(i)
        insert_value.append(str(each_station[4][hour]))
    charge_station.insert(table='stationMatrix', value=[tuple(insert_value)])
    print(insert_value)