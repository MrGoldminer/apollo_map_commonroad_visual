import csv
import xml.etree.ElementTree as ET

# 解析XML文件
tree = ET.parse('output.txt')
root = tree.getroot()

# 创建CSV文件
with open('6.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["lanelet_id", "leftBound_points", "rightBound_points"])

    # 遍历所有的lanelet元素
    for lanelet in root.iter('lanelet'):
        lanelet_id = lanelet.get('id')

        # 计算leftBound中的point数量
        leftBound = lanelet.find('leftBound')
        if leftBound is not None:
            leftBound_points = len(leftBound.findall('point'))
        else:
            print(f"No leftBound found in lanelet: {lanelet_id}")
            leftBound_points = 0

        # 计算rightBound中的point数量
        rightBound = lanelet.find('rightBound')
        if rightBound is not None:
            rightBound_points = len(rightBound.findall('point'))
        else:
            print(f"No rightBound found in lanelet: {lanelet_id}")
            rightBound_points = 0

        # 写入CSV文件
        writer.writerow([lanelet_id, leftBound_points, rightBound_points])
