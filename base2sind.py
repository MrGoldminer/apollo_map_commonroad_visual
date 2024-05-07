from xml.etree.ElementTree import Element
from xml.dom.minidom import  parseString
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from bag import add_location
from bag import add_scenarioTags
from function import process_lane_points
import time
start_time = time.time()
def parse_and_convert(filename):
    with open(filename, 'r') as file:
        data = file.read()
    # 创建XML树, 并添加根元素
    root = Element('commonRoad', {
        'timeStepSize': '0.1',
        'commonRoadVersion': '2020a',
        'author': 'Edmond Irani Liu, Fabian Höltke, Moritz Klischat',
        'affiliation': 'Technical University of Munich, Germany',
        'source': 'Scenario Factory (OpenStreetMaps, SUMO Traffic Simulator)',
        'benchmarkID': 'DEU_BadEssen-2_3_T-1',
        'date': '2020-08-23'
    })
    add_location(root)
    add_scenarioTags(root)   
    process_lane_points(root, data)
    #junctions = parse_junctions(data)    
    #add_junctions(root, junctions)
    #add_traffic_sign(root)
    #add_dynamic_obstacle(root)
    xml_str = ET.tostring(root, encoding='utf-8')
    dom = parseString(xml_str)
    with open('./data/yizhuang.xml', 'w') as f:
        f.write(dom.toprettyxml(indent="  "))    
    # 输出XML

parse_and_convert('./data/demo_base_map.txt')
end_time = time.time()
print("change base_map.txt to yizhuang.xml")
print("程序运行时间：", end_time - start_time, "秒")

