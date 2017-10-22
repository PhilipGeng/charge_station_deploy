# -*- coding : utf-8 -*-
import requests
import json
from dbapi import dbShell as db
import os
from local_path import BASE_DIR


def getBaiduGPS(coords_post):
    post_url = "http://api.map.baidu.com/geoconv/v1/?coords=%s&from=3&to=5&ak=td65yawK3uHPNnSGu1LF3r4GOZohULYe" % coords_post
    response = requests.get(url=post_url)
    try:
        result_json = json.loads(response.text)
        if result_json['status'] == 0:
            return result_json['result']
        else:
            return ''
    except Exception as e:
        print(response.status_code)
        print(e)
        return ''


def park():
    # 连接数据库
    SHParking1 = db(os.path.join(BASE_DIR, 'db/SHParking.db'))
    # 读取数据
    coords_tuple = SHParking1.select(table='ParkStaticData')
    counter = 0
    # 合并经纬度
    coords_post = ''
    # 记录停车场ID
    parkIDList = []
    # 循环获取新坐标
    for coords in coords_tuple:
        counter = counter + 1
        coords_post = coords_post + '%s,%s' % (coords[8], coords[7])
        parkIDList.append(coords[0])
        # 每100组坐标请求一次
        if counter % 100 == 0 or counter == coords_tuple.__len__():
            coords_baidu = getBaiduGPS(coords_post)
            # 如果获取成功，写入数据库
            if coords_baidu:
                for i in range(0, coords_baidu.__len__()):
                    SHParking1.insert(table='ParkBaiduGPS',
                                      value=[(parkIDList[i], coords_baidu[i]['y'], coords_baidu[i]['x'])])
                parkIDList = []
                coords_post = ''
        else:
            coords_post = coords_post + ';'


def station():
    # 连接数据库
    SHParking1 = db('/Users/chaidi/Documents/RA-Documents/EVcharge.db')
    # 读取数据
    coords_tuple = SHParking1.select(table='station_pub')
    counter = 0
    # 合并经纬度
    coords_post = ''
    # 记录停车场ID
    opid = []
    stid = []
    # 循环获取新坐标
    for coords in coords_tuple:
        counter = counter + 1
        coords_post = coords_post + '%s,%s' % (coords[5], coords[4])
        opid.append(coords[0])
        stid.append(coords[2])
        # 每100组坐标请求一次
        if counter % 100 == 0 or counter == coords_tuple.__len__():
            coords_baidu = getBaiduGPS(coords_post)
            # 如果获取成功，写入数据库
            if coords_baidu:
                for i in range(0, coords_baidu.__len__()):
                    SHParking1.insert(table='stationBaiduGPS',
                                      value=[(opid[i], stid[i], coords_baidu[i]['y'], coords_baidu[i]['x'])])
                opid = []
                stid = []
                coords_post = ''
        else:
            coords_post = coords_post + ';'


def poi2():
    # 连接数据库
    poi2 = db('/Users/chaidi/Documents/RA-Documents/poi2.db')
    # 读取数据
    coords_tuple = poi2.select(table='poi')
    counter = 0
    # 合并经纬度
    coords_post = ''
    # 循环获取新坐标
    for coords in coords_tuple:
        counter = counter + 1
        coords_post = coords_post + '%s,%s' % (coords[5], coords[4])
        # 每100组坐标请求一次
        if counter % 100 == 0 or counter == coords_tuple.__len__():
            coords_baidu = getBaiduGPS(coords_post)
            # 如果获取成功，写入数据库
            if coords_baidu:
                numbers = coords_baidu.__len__()
                for i in range(0, numbers):
                    tmp = [e for e in coords_tuple[counter - numbers + i]]
                    tmp.append(coords_baidu[i]['y'])
                    tmp.append(coords_baidu[i]['x'])
                    insert_value = tuple(tmp)
                    # insert_value = (coords[0], coords[1],coords[2],coords[3],coords[4],coords[5],coords[6],
                    #                 coords[7],coords[8],coords_baidu[i]['y'], coords_baidu[i]['x'])
                    poi2.insert(table='poiWithBaiduGPS',
                                      value=[insert_value])
                    print([insert_value])
                coords_post = ''
        else:
            coords_post = coords_post + ';'


def evs():
    # 连接数据库
    poi2 = db('/Users/chaidi/Documents/RA-Documents/EVs.db')
    # 读取数据
    coords_tuple = poi2.select(table='evstop')
    counter = 0
    # 合并经纬度
    coords_post = ''
    # 循环获取新坐标
    for coords in coords_tuple:
        counter = counter + 1
        coords_post = coords_post + '%s,%s' % (coords[4], coords[3])
        # 每100组坐标请求一次
        if counter % 100 == 0 or counter == coords_tuple.__len__():
            coords_baidu = getBaiduGPS(coords_post)
            # 如果获取成功，写入数据库
            if coords_baidu:
                numbers = coords_baidu.__len__()
                for i in range(0, numbers):
                    tmp = [e for e in coords_tuple[counter - numbers + i]]
                    tmp.append(coords_baidu[i]['y'])
                    tmp.append(coords_baidu[i]['x'])
                    insert_value = tuple(tmp)
                    # insert_value = (coords[0], coords[1],coords[2],coords[3],coords[4],coords[5],coords[6],
                    #                 coords[7],coords[8],coords_baidu[i]['y'], coords_baidu[i]['x'])
                    poi2.insert(table='evstopWithBaiduGPS',
                                      value=[insert_value])
                    print([insert_value])
                coords_post = ''
        else:
            coords_post = coords_post + ';'


def mobike():
    # 连接数据库
    poi2 = db('/Users/chaidi/Documents/RA-Documents/Mobike.db')
    # 读取数据
    coords_tuple = poi2.select(table='checkin')
    counter = 0
    # 合并经纬度
    coords_post = ''
    # 循环获取新坐标
    for coords in coords_tuple:
        counter = counter + 1
        coords_post = coords_post + '%s,%s' % (coords[4], coords[5])
        # 每100组坐标请求一次
        if counter % 100 == 0 or counter == coords_tuple.__len__():
            coords_baidu = getBaiduGPS(coords_post)
            # 如果获取成功，写入数据库
            if coords_baidu:
                numbers = coords_baidu.__len__()
                for i in range(0, numbers):
                    tmp = [e for e in coords_tuple[counter - numbers + i]]
                    tmp.append(coords_baidu[i]['y'])
                    tmp.append(coords_baidu[i]['x'])
                    insert_value = tuple(tmp)
                    # insert_value = (coords[0], coords[1],coords[2],coords[3],coords[4],coords[5],coords[6],
                    #                 coords[7],coords[8],coords_baidu[i]['y'], coords_baidu[i]['x'])
                    poi2.insert(table='checkinBaiduGPS',
                                      value=[insert_value])
                    print([insert_value])
                coords_post = ''
        else:
            coords_post = coords_post + ';'

if __name__ == '__main__':
    park()