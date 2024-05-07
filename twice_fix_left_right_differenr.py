import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json

# Step 1: 遍历XML文件中的所有lanelet元素，找出左右边界点数不等的lanelet
tree = ET.parse('./data/yizhuangfix.xml')
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
df.to_csv('./data/lanelet_points.csv', index=False)
# 找到点的最大数量
# 找到点的最大数量
# 读取数据
df = pd.read_csv('./data/lanelet_points.csv')
# 找到点的最大数量
# #贝塞尔曲线法
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from scipy.interpolate import make_interp_spline

def enhanced_process_data(row):
    def bezier_interpolate(points, num_points):
        """ Generate Bezier curve points from given points. """
        if len(points) < 2:
            return np.tile(points, (num_points, 1)) if points.size else np.zeros((num_points, 2))
        t = np.linspace(0, 1, len(points))
        t_new = np.linspace(0, 1, num_points)
        spline_x = make_interp_spline(t, points[:, 0], bc_type='natural')
        spline_y = make_interp_spline(t, points[:, 1], bc_type='natural')
        interpolated_x = spline_x(t_new)
        interpolated_y = spline_y(t_new)
        return np.column_stack((interpolated_x, interpolated_y))
    def parse_points(points):
        try:
            parsed = np.array(eval(points))
            return parsed if parsed.size else np.empty((0, 2))
        except:
            return np.empty((0, 2))

    def interpolate_points(points, method='linear', num_points=100):
        if len(points) == 1:
            # If only one point, repeat it to meet the requirement
            return np.tile(points, (num_points, 1))
        elif len(points) == 2:
            # If two points, add a middle point using average
            middle_point = np.mean(points, axis=0)
            return np.array([points[0], middle_point, points[1]])
        elif len(points) == 3:
            # Linear interpolation for three points
            t = np.linspace(0, 1, len(points))
            t_new = np.linspace(0, 1, num_points)
            spline_x = CubicSpline(t, points[:, 0], bc_type='not-a-knot')
            spline_y = CubicSpline(t, points[:, 1], bc_type='not-a-knot')
            interpolated_x = spline_x(t_new)
            interpolated_y = spline_y(t_new)
            return np.column_stack((interpolated_x, interpolated_y))
        else:
            # Bezier interpolation for four or more points
            return bezier_interpolate(points, num_points)

    left_vertices = parse_points(row['LeftPoints'])
    right_vertices = parse_points(row['RightPoints'])

    # Determine the number of points to interpolate based on the maximum of existing points
    num_points = max(len(left_vertices), len(right_vertices), 2)  # Ensure at least two points

    # Perform interpolation or addition based on the number of points
    if len(left_vertices) > 1:
        left_interpolated = interpolate_points(left_vertices, num_points=num_points)
    else:
        left_interpolated = np.tile(left_vertices, (2, 1)) if left_vertices.size else np.zeros((2, 2))
    
    if len(right_vertices) > 1:
        right_interpolated = interpolate_points(right_vertices, num_points=num_points)
    else:
        right_interpolated = np.tile(right_vertices, (2, 1)) if right_vertices.size else np.zeros((2, 2))

    return left_interpolated.tolist(), right_interpolated.tolist()

# Apply the enhanced processing function
df[['NewLeftPoints', 'NewRightPoints']] = df.apply(enhanced_process_data, axis=1, result_type='expand')

# Save the updated dataframe to a new CSV file
output_path_enhanced = './data/enhanced_processed_lanelet_points.csv'
df.to_csv(output_path_enhanced, index=False)
# Step 4: 将插值后的左右边界点和中心线点写入XML文件
# Step 5: 将修改后的左右边界点重新写入XML文件

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

