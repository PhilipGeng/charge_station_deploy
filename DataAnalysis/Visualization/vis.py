# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import re


def interface(park_analysis):
    figure_counter = 1
    park_count = 0
    while True:
        commend = input("input: parkID:*** or any num or press enter -->>")
        if commend == '':
            if park_count >= park_analysis.__len__():
                park_count %= park_analysis.__len__()
            showOnce(park_analysis[park_count])
            park_count += 1
        if re.match("\d+", commend):
            park_count = int(commend)
            if park_count >= park_analysis.__len__():
                park_count %= park_analysis.__len__()
            showOnce(park_analysis[park_count])
        parkIDMode = re.match("parkID:(.*)",commend)
        if parkIDMode:
            for park_inf in park_analysis:
                if parkIDMode.group(1) == park_inf[0]:
                    showOnce(park_analysis[park_count])


def interface_save(park_analysis):
    for park in park_analysis:
        showOnce(park, save_flag=True, show_flag=False)


def interface_altered(park_analysis):
    figure_counter = 1
    park_count = 0
    while True:
        commend = input("input: parkID:*** or any num or press enter -->>")
        if commend == '':
            if park_count >= park_analysis.__len__():
                park_count %= park_analysis.__len__()
            showOnce(park_analysis[park_count])
            park_count += 1
        if re.match("\d+", commend):
            park_count = int(commend)
            if park_count >= park_analysis.__len__():
                park_count %= park_analysis.__len__()
            showOnce(park_analysis[park_count])
        parkIDMode = re.match("parkID:(.*)", commend)
        if parkIDMode:
            for park_inf in park_analysis:
                if parkIDMode.group(1) == park_inf[0]:
                    showOnce(park_analysis[park_count])
        if re.match('^exit$', commend):
            break


def showOnce(park, save_flag = False, show_flag = True):
    parkID = park[0]
    parkName = park[1]
    parkDatas = park[2]
    hour = []
    occupancy = []
    start_date = park[2][0][0]
    start_hour = park[2][0][1]
    end_data = park[2][park[2].__len__()-1][0]
    end_hour = park[2][park[2].__len__() - 1][1]
    hour_counter = 0
    for parkData in parkDatas:
        hour.append(hour_counter)
        hour_counter += 1
        occupancy.append((float(parkData[2])))
    hour = np.array(hour)
    occupancy = np.array(occupancy)
    plt.figure(1, figsize=(20,10))
    axes = plt.subplot(111)
    plt.plot(hour, occupancy, 'bo', hour, occupancy, 'k')
    plt.xlabel('crawlTime by hour, %s %s:00 to %s %s:00' % (start_date,start_hour,end_data,end_hour))
    plt.ylabel('occupancy')
    axes.set_yticks([e/20.0 for e in range(0,21)])
    axes.set_xticks([])
    plt.title('parkID=%s' % (parkID))
    hour_counter = 0
    axis_font = {'fontname': 'Arial', 'size': '10'}
    pre_date = ''
    for parkData in parkDatas:
        if (hour_counter+1) % 3 == 0:
            plt.text(hour_counter, occupancy[hour_counter]+0.002, r'$%s$' % parkData[1], **axis_font)
        if pre_date == '' or pre_date != park[2][hour_counter][0]:
            pre_date = park[2][hour_counter][0]
            plt.text(hour_counter, 0, r'$%s$' % park[2][hour_counter][0][6:10], **axis_font)
            plt.vlines(hour_counter, 0, 1)
        hour_counter += 1
    plt.grid(True)
    if save_flag:
        plt.savefig('/Users/chaidi/Documents/RA-Documents/ParkingDataVis/%s-%s.png' % (parkID, ''.join([e for e in list(parkName) if e != '/'])))
        print('File saved in ParkingDataVis/%s-%s.png' % (parkID, ''.join([e for e in list(parkName) if e != '/'])))
    if show_flag:
        plt.show()
    plt.close()
    pass