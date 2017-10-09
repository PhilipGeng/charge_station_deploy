# _*_ coding:utf-8 _*_
import re


# 朴素匹配
def naive_match(s, p):
    m = len(s)
    n = len(p)
    for i in range(m-n+1):  # 起始指针i
        if s[i:i+n] == p:
            return True
    return False


# KMP
def kmp_match(s, p):
    if s is None or p is None:
        return 0
    if p.__len__() > s.__len__():
        tmp = s
        s = p
        p = tmp
    m = len(s)
    n = len(p)
    cur = 0  # 起始指针cur
    table = partial_table(p)
    while cur <= m-n:
        for i in range(n):
            if s[i+cur] != p[i]:
                cur += max(i - table[i-1], 1)  # 有了部分匹配表,我们不只是单纯的1位1位往右移,可以一次移动多位
                break
        else:
            return 1
    return 0


# 部分匹配表
def partial_table(p):
    '''partial_table("ABCDABD") -> [0, 0, 0, 0, 1, 2, 0]'''
    prefix = set()
    postfix = set()
    ret = [0]
    for i in range(1,len(p)):
        prefix.add(p[:i])
        postfix = {p[j:i+1] for j in range(1,i+1)}
        ret.append(len((prefix&postfix or {''}).pop()))
    return ret


def matching_address(parkName, stationName, park_address, station_address, distance):
    park_address = park_address.replace(' ', '')
    station_address = station_address.replace(' ', '')
    match1 = re.match('(.*市市辖区)?(.*市)?(.*?区)?(.*?路)?(.*?街)?(.*?弄)?(.*?号)?(.*)', park_address)
    n = 3
    if match1:
        park_item1 = match1.group(1)
        park_item2 = match1.group(n)
        park_item3 = match1.group(n+1)
        park_item4 = match1.group(n+2)
        park_item5 = match1.group(n+3)
        park_item6 = match1.group(n+4)
        park_item7 = match1.group(n+5)
    match2 = re.match('(.*市市辖区)?(.*市)?(.*?区)?(.*?路)?(.*?街)?(.*?弄)?(.*?号)?(.*)', station_address)
    if match1:
        station_item1 = match2.group(1)
        station_item2 = match2.group(n)
        station_item3 = match2.group(n+1)
        station_item4 = match2.group(n+2)
        station_item5 = match2.group(n+3)
        station_item6 = match2.group(n+4)
        station_item7 = match2.group(n+5)
    sim1 = kmp_match(park_item2, station_item2)
    sim2 = kmp_match(park_item3, station_item3)
    sim3 = kmp_match(park_item4, station_item4)
    sim4 = kmp_match(park_item5, station_item5)
    sim5 = 1 if park_item6 is not None and station_item6 is not None and park_item6 == station_item6 else 0

    sim_name = kmp_match(parkName, stationName)
    # print(sim1, sim2, sim3, sim4, sim5)
    similarity = 0.1 * sim1 + 0.4 * (sim2 + sim3) + 0.1 * sim4 + 0.4 * sim5
    similarity2 = 40 / float(distance) + 0.6 * sim_name
    if similarity >= 0.8:
        return 2
    if similarity2 >= 0.8:
        return 1
    return 0

if __name__ == '__main__':
    c = '虹口区同丰路669号'
    a = '天山衡辰公寓停车场'
    b = '缤谷文化休闲广场'
    d = '望园南路1288弄'
    e = 201.101963909402
    print(matching_address(a, b, c, d, e))
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #
    # park_db = db(os.path.join(BASE_DIR, 'db/SHParking.db'))
    #
    # station_db = db(os.path.join(BASE_DIR, 'db/EVcharge.db'))
    #
    # station_adds = station_db.select(table='station_pub', cols='address')
    #
    # park_adds = park_db.select(table='ParkStaticData', cols='address')
    #
    # add_num = station_adds.__len__()
    # counter = 0
    # for park_add in park_adds:
    #     for station_add in station_adds:
    #         if matching_address(park_add[0], station_add[0]):
    #             counter += 1
    #             print("SUCCEED")
    # print(counter)
