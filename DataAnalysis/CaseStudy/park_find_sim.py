# _*_ coding:utf-8 _*_

import os

from dbapi import dbShell as db
from local_path import dbPath

park_db = db(os.path.join(dbPath + 'SHParking.db'))

parkIDs = [
    # 'hk31010900001',
    # 'hp31010100048',
    # 'hp31010100069',
    # 'xh31010400124',
    # 'xh31010400247',
    # 'xh31010400103',
    # 'xh31010400019',
    # 'xh31010400250',
    'hp31010100134',
]
final_result = {}
for parkID in parkIDs:
    records = park_db.select(table='park_similarity', condition="parkID1='%s'" % parkID,
                             orderby='similarity+0')
    result = records[1:6]
    final_result[parkID] = result
    print("#############################")
    for e in result:
        parkID2 = e[1]
        
    print("#############################")
print(final_result)
