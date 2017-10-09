# -*- coding:utf-8 -*-
import re
from dbapi import dbShell as db
import os
from local_path import BASE_DIR


def get_data():
    EVcharge = db(os.path.join(BASE_DIR, 'db/EVcharge.db'))
    raw_data = EVcharge.select(table='data_pub',
                               cols='time,stid,opid,directtotal,directavailable,altertotal,alteravailable',
                               orderby='stid,time')
    EVcharge.close()
    return raw_data


def compute_occupancy(raw_data):
    total_data = []
    old_stid = None
    old_opid = None
    each_st = []
    dir_occupancy = 0
    alt_occupancy = 0
    total_occupancy = 0
    occ_counter = 0
    old_hour = None
    old_date = None
    counter = 0
    for record in raw_data:
        counter += 1
        # 提取日期与小时
        time_match = re.match("(.*) (\d\d):.*", record[0])
        if time_match:
            date = time_match.group(1)
            hour = time_match.group(2)
        # 获取 stid 和 opid
        stid = record[1]
        opid = record[2]
        dir_total = record[3]
        alt_total = record[5]
        dir_occ = 0.0 if dir_total == 0 else (1 - float(record[4]) / float(record[3]))
        alt_occ = 0.0 if alt_total == 0 else (1 - float(record[6]) / float(record[5]))
        total_occ = 0.0 if alt_total == 0 and dir_total == 0 else (
           1 - (float(record[4]) + float(record[6])) / (float(record[3]) + float(record[5]))
        )
        if old_hour is None:
            old_hour = hour
            old_date = date
        # 如果新纪录与上一个记录的日期或者小时不同，则计算上一个记录的平均占用率
        if old_hour != hour or old_date != date:
            # 计算直流-交流-总体占用率
            dir_occupancy = dir_occupancy/occ_counter
            alt_occupancy = alt_occupancy/occ_counter
            total_occupancy = total_occupancy / occ_counter
            # 放入List，每个充电桩每小时有一个List
            each_st.append((old_date, old_hour, '%.3f' % total_occupancy, '%d' % (dir_total + alt_total)))
            # clear record
            dir_occupancy = 0
            occ_counter = 0
            alt_occupancy = 0
            total_occupancy = 0
            old_date = date
            old_hour = hour
        # 累加同一充电站每小时的占用率，用于求平均
        dir_occupancy = dir_occupancy + dir_occ
        alt_occupancy = alt_occupancy + alt_occ
        total_occupancy = total_occupancy + total_occ
        # 计数器，用于求平均
        occ_counter += 1
        if old_stid is None:
            old_stid = stid
            old_opid = opid
        # 如果新纪录的两个主键有一个与上一个记录不同，将上一个充电站保存到total_data中
        if old_stid != stid or old_opid != opid or counter == raw_data.__len__():
            total_data.append((old_stid, old_opid, each_st))
            each_st = []
            old_stid = stid
            old_opid = opid

    return total_data


def save_data(values):
    EVcharge = db(os.path.join(BASE_DIR, 'db/EVcharge.db'))
    for value in values:
        stid = value[0]
        opid = value[1]
        for record in value[2]:
            try:
                EVcharge.insert(table='stationOcc',
                                value=[(stid, opid, record[0], record[1], record[2], record[3])])
            except Exception:
                print('error occured at station: %s' % stid)
        print('stid:%s opid:%s is inserted' % (stid, opid))
    EVcharge.close()


if __name__ == '__main__':
    raw_data = get_data()
    occ_data = compute_occupancy(raw_data)
    save_data(occ_data)
