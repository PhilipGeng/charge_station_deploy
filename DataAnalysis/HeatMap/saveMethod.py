# _*_ coding:utf-8 _*_
import re

# save data
# matrix 一行代表纬度，即转置前
# fileName 为带路径的文件名
def save_txt(matrix, fileName):
    # 生成变量名
    match_re = re.match('.*/(.*).txt', fileName)
    if match_re:
        varName = match_re.group(1)
    else:
        varName = fileName
    ####################################################################################################
    # 数据定义，拷贝过来的
    ####################################################################################################
    lngperkm = 0.009
    latperkm = 0.0103
    # 计算格子中心用
    half_latperkm = latperkm / 2
    half_lngperkm = lngperkm / 2
    bottom = 30.408258525468
    top = 32.408258525468
    left = 120.22177414094
    right = 122.22177414094
    latgridnum = int((top - bottom) / latperkm)
    lnggridnum = int((right - left) / lngperkm)
    ####################################################################################################
    # 先拼接每行的字符串，再逐行写入文件
    # 文件格式：
    # var parm = [
    #   [{"lat":value, "lng":value, "count":number},{} ......],
    #   [{},{} ......],
    #   .
    #   .
    # ]
    ####################################################################################################
    center_positions = []
    line_position = ''
    for i in range(0, latgridnum):
        lat = top - half_latperkm - i * latperkm
        for j in range(0, lnggridnum):
            lng = left + half_lngperkm + j * lngperkm
            line_position += '{"lat":%s,"lng":%s,"count":%s},' % (lat, lng, matrix[i, j])
        center_positions.append(line_position)
        line_position = ''
    with open(fileName, 'w') as f:
        first_line = "var %s = [\n" % varName
        last_line = "]"
        f.write(first_line)
        for each_line in center_positions:
            each_line = '[' + each_line[:-1] + '],\n'  # [:-1]去除最后一个逗号
            f.write(each_line)
        f.write(last_line)
    f.close()