import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json

# Step 1: 遍历XML文件中的所有lanelet元素，找出左右边界点数不等的lanelet
tree = ET.parse('./data/yizhuang.xml')
root = tree.getroot()
data = []
for lanelet in root.findall('lanelet'):
    leftBound_points = list(lanelet.find('leftBound').findall('point'))
    rightBound_points = list(lanelet.find('rightBound').findall('point'))
    if len(leftBound_points) != len(rightBound_points):
        # 提取左右边界的所有点的坐标
        left_points = np.array([[float(point.find('x').text), float(point.find('y').text)] for point in leftBound_points])
        right_points = np.array([[float(point.find('x').text), float(point.find('y').text)] for point in rightBound_points])
        data.append([lanelet.get('id'), len(leftBound_points), len(rightBound_points), left_points.tolist(), right_points.tolist()])

# Step 2: 对于每个找到的lanelet，提取其ID和不相等的坐标，并将这些信息存储在一个numpy数组中
data = np.array(data, dtype=object)
# Step 3: 将numpy数组保存为CSV文件
df = pd.DataFrame(data, columns=['LaneletID', 'LeftBoundPoints', 'RightBoundPoints', 'LeftPoints', 'RightPoints'])
df['LeftPoints'] = df['LeftPoints'].apply(json.dumps)
df['RightPoints'] = df['RightPoints'].apply(json.dumps)
df.to_csv('lanelet_points.csv', index=False)

# 找到点的最大数量
# 找到点的最大数量
# 读取数据
df = pd.read_csv('lanelet_points.csv')
# Re-import numpy to ensure it's available in the function
import numpy as np

def interpolate_points(left_points, right_points):
    # Parsing string representations to actual lists of tuples (numpy arrays)
    left_array = np.array(eval(left_points))
    right_array = np.array(eval(right_points))
    
    num_left = len(left_array)
    num_right = len(right_array)
    max_points = max(num_left, num_right)
    
    def interpolate_to_fit(source_array, target_length):
        if len(source_array) == target_length:
            return source_array
        interp_indices = np.linspace(0, len(source_array) - 1, target_length)
        interp_x = np.interp(interp_indices, np.arange(len(source_array)), source_array[:, 0])
        interp_y = np.interp(interp_indices, np.arange(len(source_array)), source_array[:, 1])
        return np.vstack((interp_x, interp_y)).T

    new_left = interpolate_to_fit(left_array, max_points)
    new_right = interpolate_to_fit(right_array, max_points)
    
    return new_left.tolist(), new_right.tolist()

# Apply interpolation to each row
df[['NewLeftPoints', 'NewRightPoints']] = df.apply(lambda row: interpolate_points(row['LeftPoints'], row['RightPoints']), axis=1, result_type='expand')

# Save the updated dataframe to a new CSV file
output_path = 'updated_lanelet_points.csv'
df.to_csv(output_path, index=False)

# Step 5: 将新的坐标插入到原XML文件中的相应lanelet的point下
for index, row in df.iterrows():
    lanelet = root.find(f"lanelet[@id='{row['LaneletID']}']")
    if lanelet is not None:
        leftBound = lanelet.find('leftBound')
        rightBound = lanelet.find('rightBound')
        # 删除原有的point元素
        for point in leftBound.findall('point'):
            leftBound.remove(point)
        for point in rightBound.findall('point'):
            rightBound.remove(point)
        # 插入新的point元素
        for point in row['NewLeftPoints']:
            new_point = ET.SubElement(leftBound, 'point')
            ET.SubElement(new_point, 'x').text = str(point[0])
            ET.SubElement(new_point, 'y').text = str(point[1])
        for point in row['NewRightPoints']:
            new_point = ET.SubElement(rightBound, 'point')
            ET.SubElement(new_point, 'x').text = str(point[0])
            ET.SubElement(new_point, 'y').text = str(point[1])
# 将修改后的XML树写入文件
tree.write('./data/output.xml')
