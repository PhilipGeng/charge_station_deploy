# _*_coding:utf:8_*_
import os

from Visualization.vis import *
from dbapi import dbShell as db
from local_path import BASE_DIR



# 求停车场每小时平均占用率
def handle_park_data(parks):
    park_analysis = []
    each_park = []
    old_park_id = None
    old_park_name = None
    occupancy_hour = 0
    sum_count = 0
    old_hour = None
    old_date = None
    counter = 0
    for park in parks:
        counter += 1
        occupancy_min = (float(park[3]) / float(park[4]))
        hour_match = re.match(".*?(\d\d):.*", park[2])
        if hour_match:
            hour = hour_match.group(1)
        date_match = re.match("(.*) .*", park[2])
        if date_match:
            date = date_match.group(1)

        if old_park_id is None:
            old_park_id = park[0]
            old_park_name = park[1]
        if old_park_id != park[0] or counter == parks.__len__():
            park_analysis.append((old_park_id, old_park_name, each_park))
            each_park = []
            old_park_id = park[0]
            old_park_name = park[1]

        if old_hour is None:
            old_hour = hour
            old_date = date
        if old_hour != hour or old_date != date:
            # 计算占用率
            occupancy_hour = 1 - (occupancy_hour / sum_count)
            each_park.append((old_date, old_hour, occupancy_hour))
            occupancy_hour = 0
            sum_count = 0
            old_hour = hour
            old_date = date
        occupancy_hour = occupancy_hour + occupancy_min
        sum_count += 1
    return park_analysis


# 存储停车场每小时占用率
def analysis_and_store_data(SHParking1):
    park1 = SHParking1.select(table="park",
                              cols="parkID,parkName,crawlTime,surplusQuantity,totalNum",
                              condition='surplusQuantity!="-1" and surplusQuantity<totalNum ',
                              orderby="parkID")

    park1_analysis = handle_park_data(park1)

    for park in park1_analysis:
        parkID = park[0]
        parkName = park[1]
        for record in park[2]:
            SHParking1.insert(table='ParkOcc', value=[(parkID, parkName, record[0], record[1], record[2])])
            print([(parkID, parkName, record[0], record[1], record[2])])
    return park1_analysis


# 将数据库中的数据进行整理，存储到list中，结构如下：
#
# [(parkID, parkName, [(date, hour, occupancy)...]),....]
#
def combine_data(park_occs):
    parkID_total = {}
    park_analysises = []
    counter = 0
    for park_occ in park_occs:
        if park_occ[0] in parkID_total:
            park_analysises[parkID_total[park_occ[0]]][2].append((park_occ[2], park_occ[3], park_occ[4]))
        else:
            parkID_total[park_occ[0]] = counter
            counter += 1
            park_analysises.append((park_occ[0], park_occ[1],[(park_occ[2], park_occ[3], park_occ[4])]))
    return park_analysises


ANALYSIS_DATA = True
SAVE_DATA = False


if __name__ == '__main__':

    SHParking1 = db(os.path.join(BASE_DIR, 'db/SHParking.db'))

    if ANALYSIS_DATA:
        park_analysis = analysis_and_store_data(SHParking1)
        # interface(park1_analysis)
    else:
        park_occs = SHParking1.select(table='ParkOcc', condition='occupancy<"1"')
        park_analysis = combine_data(park_occs)

    if SAVE_DATA:
        interface_save(park_analysis)



