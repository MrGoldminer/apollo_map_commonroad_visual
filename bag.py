import re
from xml.etree.ElementTree import SubElement, tostring
from xml.dom import minidom
import random
import xml.etree.ElementTree as ET
def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_location(root):
    # 添加location元素
    location = ET.SubElement(root, 'location')
    ET.SubElement(location, 'geoNameId').text = '2953464'
    ET.SubElement(location, 'gpsLatitude').text = '52.31667'
    ET.SubElement(location, 'gpsLongitude').text = '8.33333'

#def process_boundary_points(boundary, points_string, points_pattern):
    #for point_match in points_pattern.finditer(points_string):
        #point = SubElement(boundary, 'point')
        #SubElement(point, 'x').text = point_match.group('x')
        #SubElement(point, 'y').text = point_match.group('y')
def process_boundary_points(boundary, points_string, points_pattern):
    for point_match in points_pattern.finditer(points_string):
        point = SubElement(boundary, 'point')
        SubElement(point, 'x').text = point_match.group('x')
        SubElement(point, 'y').text = point_match.group('y')
        # Now also process the z-coordinate
        #SubElement(point, 'z').text = point_match.group('z')

def add_scenarioTags(root):
    # 添加scenarioTags元素
    scenarioTags = ET.SubElement(root, 'scenarioTags')
    ET.SubElement(scenarioTags, 'intersection')
    ET.SubElement(scenarioTags, 'simulated')
    ET.SubElement(scenarioTags, 'critical')

def add_dynamic_obstacle(root):
    dynamic_obstacle = SubElement(root, 'dynamicObstacle', id='23461')
    SubElement(dynamic_obstacle, 'type').text = 'motorcycle'
    shape = SubElement(dynamic_obstacle, 'shape')
    rectangle = SubElement(shape, 'rectangle')
    SubElement(rectangle, 'length').text = '2.5'
    SubElement(rectangle, 'width').text = str(random.uniform(0.7, 0.8))
    initial_state = SubElement(dynamic_obstacle, 'initialState')
    position = SubElement(initial_state, 'position')
    point = SubElement(position, 'point')
    SubElement(point, 'x').text = str(random.uniform(970, 980))
    SubElement(point, 'y').text = str(random.uniform(-160, -150))
    SubElement(initial_state, 'orientation', exact=str(random.uniform(2.8, 2.9)))
    SubElement(initial_state, 'time', exact='0')
    SubElement(initial_state, 'velocity', exact=str(random.uniform(2.0, 2.1)))
    SubElement(initial_state, 'acceleration', exact=str(random.uniform(-0.03, -0.02)))
    trajectory = SubElement(dynamic_obstacle, 'trajectory')
    for _ in range(4):
        state = SubElement(trajectory, 'state')
        position = SubElement(state, 'position')
        point = SubElement(position, 'point')
        SubElement(point, 'x').text = str(random.uniform(970, 980))
        SubElement(point, 'y').text = str(random.uniform(-160, -150))
        SubElement(state, 'orientation', exact=str(random.uniform(2.8, 2.9)))
        SubElement(state, 'time', exact=str(random.randint(1, 4)))
        SubElement(state, 'velocity', exact=str(random.uniform(1.9, 2.0)))
        SubElement(state, 'acceleration', exact=str(random.uniform(-0.09, -0.08)))

def add_traffic_sign(root):
    traffic_sign = SubElement(root, 'trafficSign', id=str(random.randint(22000, 23000)))
    traffic_sign_element = SubElement(traffic_sign, 'trafficSignElement')
    SubElement(traffic_sign_element, 'trafficSignID').text = str(random.randint(250, 300))
    SubElement(traffic_sign_element, 'additionalValue').text = str(random.uniform(1.0, 2.0))
    position = SubElement(traffic_sign, 'position')
    point = SubElement(position, 'point')
    SubElement(point, 'x').text = str(random.uniform(950, 960))
    SubElement(point, 'y').text = str(random.uniform(-180, -170))
    SubElement(traffic_sign, 'virtual').text = 'false'

def add_intersection(root):
    intersection = SubElement(root, 'intersection', id=str(random.randint(24000, 25000)))
    for _ in range(4):
        incoming = SubElement(intersection, 'incoming', id=str(random.randint(24000, 25000)))
        SubElement(incoming, 'incomingLanelet', ref=str(random.randint(22000, 23000)))
        SubElement(incoming, 'successorsRight', ref=str(random.randint(22000, 23000)))
        SubElement(incoming, 'successorsStraight', ref=str(random.randint(22000, 23000)))
        SubElement(incoming, 'successorsLeft', ref=str(random.randint(22000, 23000)))

def parse_junctions(text):
    junctions = {}
    junction_id = None
    for line in text.split('\n'):
        match = re.search(r'overlap_junction_(\w+)_lane_(\d+)', line)
        if match:
            junction_id = match.group(1)
            lane_id = match.group(2)
            if junction_id not in junctions:
                junctions[junction_id] = []
            junctions[junction_id].append(lane_id)
    return junctions

def add_junctions(root, junctions):
    added_lane_ids = set()  # 用于跟踪已经添加到XML中的lane_id
    for junction_id, lane_ids in junctions.items():
        # 提取junction_id中的数字并加上100
        num = int(re.search(r'\d+', junction_id).group()) + 100
        intersection = SubElement(root, 'intersection')
        intersection.set('id', str(num))  # 将数字转换为字符串并设置为id属性
        
        for i, lane_id in enumerate(lane_ids):
            if lane_id not in added_lane_ids:
                incoming = SubElement(intersection, 'incoming')
                incoming.set('id', str(int(lane_ids[i]) + 20000))
                added_lane_ids.add(lane_id)  # 标记lane_id已添加
                
                incomingLanelet = SubElement(incoming, 'incomingLanelet')
                incomingLanelet.set('ref', lane_ids[(i+1)%len(lane_ids)])
                
                successorsRight = SubElement(incoming, 'successorsRight')
                successorsRight.set('ref', lane_ids[(i+2)%len(lane_ids)])
                
                successorsStraight = SubElement(incoming, 'successorsStraight')
                successorsStraight.set('ref', lane_ids[(i+3)%len(lane_ids)])
                
                successorsLeft = SubElement(incoming, 'successorsLeft')
                successorsLeft.set('ref', lane_ids[i%len(lane_ids)])  
# 使用取模运算符来循环索引
