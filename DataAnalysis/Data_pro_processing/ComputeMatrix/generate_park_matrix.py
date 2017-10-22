import os

from dbapi import dbShell as db
from local_path import BASE_DIR


error_contral = 0.5

def combine_data(park_occs):
    parkID_total = {}
    park_analysises = []
    counter = 0
    for park_occ in park_occs:
        if  park_occ[0] in parkID_total:
            park_analysises[parkID_total[park_occ[0]]][2].append((park_occ[2], park_occ[3], park_occ[4]))
        else:
            parkID_total[park_occ[0]] = counter
            counter += 1
            park_analysises.append((park_occ[0], park_occ[1],[(park_occ[2], park_occ[3], park_occ[4])]))
    return park_analysises


def repaire_data(record):
    hours = ['00', '01', '02', '03', '04', '05', '06',
            '07', '08', '09', '10', '11', '12', '13',
            '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23']
    for counter in range(0,24):
        if hours[counter] in record:
            pass
        else:
            left = None
            right = None
            # left
            for i in range(counter - 1, -1, -1):
                if hours[i] in record:
                    left = record[hours[i]]
                    break
            # left
            for i in range(counter + 1, 24):
                if hours[i] in record:
                    right = record[hours[i]]
                    break

            if left is None and right is not None:
                record[hours[counter]] = right
            elif right is None and left is not None:
                record[hours[counter]] = left
            elif left is not None and right is not None:
                record[hours[counter]] = (left+right) / 2
            else:
                record[hours[counter]] = -1
    return record


def fix_data(data):
    hours = ['00', '01', '02', '03', '04', '05', '06',
             '07', '08', '09', '10', '11', '12', '13',
             '14', '15', '16', '17', '18', '19', '20',
             '21', '22', '23']
    for hour in hours:
        if hour not in data:
            data[hour] = -1


def store_data_in_matrix(park_analysis, database):
    occ_hour_weekday = {}
    occ_hour_weekend = {}
    counter_weekday = {}
    counter_weekend = {}
    matlabID = 0
    for data in park_analysis:
        parkID = data[0]
        for record in data[2]:
            if record[0] == '2017-09-02' or record[0] == '2017-09-03':
                hour = record[1]
                if record[1] in occ_hour_weekend:
                    occ_hour_weekend[hour] = occ_hour_weekend[hour] + float(record[2])
                    counter_weekend[hour] += 1
                else:
                    occ_hour_weekend[hour] = float(record[2])
                    counter_weekend[hour] = 1
            else:
                hour = record[1]
                if record[1] in occ_hour_weekday:
                    occ_hour_weekday[hour] = occ_hour_weekday[hour] + float(record[2])
                    counter_weekday[hour] += 1
                else:
                    occ_hour_weekday[hour] = float(record[2])
                    counter_weekday[hour] = 1
        for hour in occ_hour_weekday:
            occ_hour_weekday[hour] = occ_hour_weekday[hour] / counter_weekday[hour]
        for hour in occ_hour_weekend:
            occ_hour_weekend[hour] = occ_hour_weekend[hour] / counter_weekend[hour]

        # fix_data(occ_hour_weekday)
        # fix_data(occ_hour_weekend)
        if occ_hour_weekday.__len__() > (24*error_contral) and occ_hour_weekend.__len__() > (24*error_contral):
            error1 = 24 - occ_hour_weekday.__len__()
            error2 = 24 - occ_hour_weekend.__len__()
            repaire_data(occ_hour_weekend)
            repaire_data(occ_hour_weekday)
            park_type = database.select(table='ParkStaticData', cols='parkType,totalNum', condition='parkID="%s"' % parkID)
            for type in park_type:
                totalNum = int(type[1])
                if "社会" in type[0]:
                    table = 'matrix_society'
                    parkType = 1
                else:
                    table = 'matrix_road'
                    parkType = 0
            matlabID += 1
            database.insert(table = 'parkMatrix',
                        value=[(parkID, matlabID, totalNum, -1,
                                occ_hour_weekday['00'], occ_hour_weekday['01'], occ_hour_weekday['02'],
                                occ_hour_weekday['03'], occ_hour_weekday['04'], occ_hour_weekday['05'],
                                occ_hour_weekday['06'], occ_hour_weekday['07'], occ_hour_weekday['08'],
                                occ_hour_weekday['09'], occ_hour_weekday['10'], occ_hour_weekday['11'],
                                occ_hour_weekday['12'], occ_hour_weekday['13'], occ_hour_weekday['14'],
                                occ_hour_weekday['15'], occ_hour_weekday['16'], occ_hour_weekday['17'],
                                occ_hour_weekday['18'], occ_hour_weekday['19'], occ_hour_weekday['20'],
                                occ_hour_weekday['21'], occ_hour_weekday['22'], occ_hour_weekday['23'],
                                occ_hour_weekend['00'], occ_hour_weekend['01'], occ_hour_weekend['02'],
                                occ_hour_weekend['03'], occ_hour_weekend['04'], occ_hour_weekend['05'],
                                occ_hour_weekend['06'], occ_hour_weekend['07'], occ_hour_weekend['08'],
                                occ_hour_weekend['09'], occ_hour_weekend['10'], occ_hour_weekend['11'],
                                occ_hour_weekend['12'], occ_hour_weekend['13'], occ_hour_weekend['14'],
                                occ_hour_weekend['15'], occ_hour_weekend['16'], occ_hour_weekend['17'],
                                occ_hour_weekend['18'], occ_hour_weekend['19'], occ_hour_weekend['20'],
                                occ_hour_weekend['21'], occ_hour_weekend['22'], occ_hour_weekend['23']
                                )])
            # database.insert(table='parkTotalNum', value=[(parkID, matlabID, parkType, totalNum, error1, error2)])

        occ_hour_weekday = {}
        occ_hour_weekend = {}
        counter_weekday = {}
        counter_weekend = {}


if __name__ == '__main__':
    park = True
    if park:
        SHParking1 = db(os.path.join(BASE_DIR, 'db/SHParking.db'))
        park_occs = SHParking1.select(table='ParkOcc', condition='occupancy<"1"')
        park_analysis = combine_data(park_occs)
        store_data_in_matrix(park_analysis, SHParking1)

    pass