# _*_ coding:utf-8 _*_
import math
from dbapi import dbShell as db
from local_path import dbPath

park_db = db(dbPath + 'SHParking.db')
station_db = db(dbPath + 'EVcharge.db')

park_matrix = park_db.select(table='parkMatrix_wash')


def compute_distance(park1, park2):
    result = 0
    for i in range(0, park1.__len__()):
        a = float(park1[i])
        b = float(park2[i])
        result = result + (a-b) * (a-b)
    return result

park_obj_nums = park_matrix.__len__()

for i in range(0, park_obj_nums):
    parkID1 = park_matrix[i][0]
    park_matrix1 = park_matrix[i][4:52]
    print("%s is done" % i)
    for j in range(0, park_obj_nums):
        parkID2 = park_matrix[j][0]
        park_matrix2 = park_matrix[j][4:52]
        try:
            similarity = compute_distance(park_matrix1, park_matrix2)
            similarity = math.sqrt(similarity)
        except Exception:
            print(parkID1, parkID2, Exception)
        map_result = station_db.select(table='map', cols='chargeNum', condition="parkID='%s'" % parkID2)
        map_result = map_result[0][0] if map_result[0][0] is not '' else '-1'
        park_db.insert(table='park_similarity', value=[(parkID1, parkID2, map_result, similarity)])