# _*_ coding:utf-8 _*_
from dbapi import dbShell as db
import numpy as np
import os
from local_path import dbPath

park_db = db(dbPath + 'SHParking.db')
station_db = db(dbPath + 'EVcharge.db')


parkIDs = [
    "hp31010100048",
    "hp31010100069",
    "xh31010400124",
    "xh31010400247",
    "xh31010400103",
    "xh31010400019",
    "xh31010400250",
    "hp31010100134",
    "hp31010100024",
    "ja31010600010",
    "ja31010600047",
    "pd31011500090",
    "pd31011500505",
    "pt31010700189",
    "pt31010700138",
    "3101010167",
    "hp31010100205",
    "hp31010100124",
    "hp31010100128",
    "hp31010100154",
]


def avg_list(value):
    value = [float(e) for e in value]
    result = 0
    for e in value:
        result = result + e
    result = result / value.__len__()
    return result


def avg_dic(value):
    result = 0
    for key in value:
        result = result + float(value[key])
    result = result / value.__len__()
    return result

# finial_result
# key = parkID
prediction = {}
x_save = []
# 2 4 6 8
increase_num = [2, 4, 6, 8]
# 加权平均数量
n = 5
count_k = increase_num.__len__()
# parkID为所有要预测的park
weekday = '"workday": [["2", %.2f], ["4", %.2f], ["6", %.2f], ["8", %.2f]],'
holiday = '"holiday": [["2", %.2f], ["4", %.2f], ["6", %.2f], ["8", %.2f]],'
weekday_sd = '"workday_sd": [["2", %.2f], ["4", %.2f], ["6", %.2f], ["8", %.2f]],'
holiday_sd = '"holiday_sd": [["2", %.2f], ["4", %.2f], ["6", %.2f], ["8", %.2f]],'

with open('data.txt', 'w') as f:
    for parkID in parkIDs:
        parkLocation = park_db.select(table='ParkBaiduGPS',
                                      cols='lat,lng',
                                      condition='parkID="%s"' % parkID)
        for location in parkLocation:
            parkLat = location[0]
            parkLng = location[1]
        # "id”:”hk3101090001”,
        # "charge_num”:4,
        # "avg_rate”:0.58,
        # "workday": [[“2”, 0.59], [“4”, 0.53], [“6”, 0.63], [“8”, 0.49]],
        # "holiday": [[“2”, 0.61], [“4”, 0.52], [“6”, 0.64], [“8”, 0.48]],
        print('#################################################################')
        print('"id":"%s",' % parkID)
        line1 = '"id":"%s",' % parkID
        map_parkid = station_db.select(table='map', condition="parkID='%s'" % parkID)
        x = int(map_parkid[0][55]) if map_parkid[0][53] is not '' else 0
        print('"charge_num":%s,' % x)
        line2 = '"charge_num":%s,' % x
        Rx_w = avg_list(map_parkid[0][56:80]) if map_parkid[0][53] is not '' else 0
        Rx_h = avg_list(map_parkid[0][80:104]) if map_parkid[0][53] is not '' else 0
        print('"avg_rate_weekday":%s,' % Rx_w)
        print('"avg_rate_holiday":%s,' % Rx_h)
        line3 = '"avg_rate_weekday":%s,' % Rx_w
        line4 = '"avg_rate_holiday":%s,' % Rx_h
        # 分别对增加 2 4 6 8个充电桩的使用率进行预测
        prediction_each_w = {}
        prediction_each_h = {}
        # Rk
        Rk_w = {}
        Rk_h = {}
        v = {}
        SD_w = {}
        SD_h = {}
        for increase in increase_num:
            v[str(increase)] = []
            records = park_db.select(table='park_similarity',
                                     condition="parkID1='%s' and parkID2!='%s' and chargeNum='%s'" %
                                               (parkID, parkID, increase),
                                     orderby='similarity+0 ASC',
                                     cols='parkID2,similarity')
            real_n = n if records.__len__() >= 5 else records.__len__()
            records = records[0:n]
            # print(records)
            # for record in records:
            #     print(record[0], 1/float(record[1]))
            # print('\n')
            # Rk numerator
            numerator_w = 0
            numerator_h = 0
            # Rk denominator
            denominator_w = 0
            denominator_h = 0
            for record in records:
                # get data
                nearby_ID = record[0]
                similarity = 1 / float(record[1])
                map_result = station_db.select(table='map',
                                               condition="parkID='%s'" % nearby_ID)
                charge_occ_w = map_result[0][56:80]
                charge_occ_h = map_result[0][80:104]
                v[str(increase)].append([nearby_ID, str(similarity), str(avg_list(charge_occ_w)),
                                         str(avg_list(charge_occ_h))])
                # compute numerator and denominator
                denominator_w = denominator_w + similarity
                numerator_w = numerator_w + similarity * avg_list(charge_occ_w)
                denominator_h = denominator_h + similarity
                numerator_h = numerator_h + similarity * avg_list(charge_occ_h)
            Rk_w[str(increase)] = numerator_w / denominator_w
            Rk_h[str(increase)] = numerator_h / denominator_h
        #################################################################
        #################################################################
        Rk_avg_w = avg_dic(Rk_w)
        Rk_avg_h = avg_dic(Rk_h)
        for key in Rk_w:
            Rk_w[key] = Rk_w[key] + (0.6 - Rk_avg_w)
            Rk_h[key] = Rk_h[key] + (0.6 - Rk_avg_h)
        for increase in increase_num:
            w = []
            h = []
            for item in v[str(increase)]:
                w.append(float(item[2]))
                h.append(float(item[3]))
            w_np = np.array(w)
            h_np = np.array(h)
            SD_w[str(increase)] = np.std(w_np)
            SD_h[str(increase)] = np.std(h_np)
        for increase in increase_num:
            # R(x+k)
            a = (x * Rx_w + increase * Rk_w[str(increase)])
            b = (x + increase)
            prediction_each_w[str(increase)] = a / b
            a = (x * Rx_h + increase * Rk_h[str(increase)])
            b = (x + increase)
            prediction_each_h[str(increase)] = a / b
        line5 = weekday %\
                (prediction_each_w['2'],
                 prediction_each_w['4'],
                 prediction_each_w['6'],
                 prediction_each_w['8'])
        line6 = holiday %\
                (prediction_each_h['2'],
               prediction_each_h['4'],
               prediction_each_h['6'],
               prediction_each_h['8'])
        line7 = weekday_sd % \
                (SD_w['2'],
                 SD_w['4'],
                 SD_w['6'],
                 SD_w['8'])
        line8 = holiday_sd % \
                (SD_h['2'],
                 SD_h['4'],
                 SD_h['6'],
                 SD_h['8'])
        print(line5)
        print(line6)
        print(line7)
        print(line8)
        f.write('{' + '\n')
        f.write(line1 + '\n')
        f.write(line2 + '\n')
        f.write(line3 + '\n')
        f.write(line4 + '\n')
        f.write(line5 + '\n')
        f.write(line6 + '\n')
        f.write(line7 + '\n')
        f.write(line8 + '\n')
        f.write('"latlng":[%s,%s],' % (parkLat, parkLng) + '\n')
        f.write('},'+ '\n')
    f.close()