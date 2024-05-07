import re
from bag import process_boundary_points
from xml.etree.ElementTree import SubElement
def extract_lane_by_id(data, lane_id):
#search for lane_info by lane_id from data
    data = './data/demo_base_map.txt'
    with open(data, 'r') as file:
        file_content = file.read()
    # 正则表达式用于找到匹配的 lane 块的开始部分
    pattern = re.compile(r'\blane {\s+id {\s+id: "lane_' + str(lane_id) + r'"\s+}', re.DOTALL)
    match = pattern.search(file_content)
    if not match:
        return "No information found for lane_id {}.".format(lane_id)
    # 找到匹配后，从该位置开始提取整个 lane 块
    start_index = match.start()
    end_index = match.end()

    # 初始化大括号计数器。已找到 lane 块起始部分，故初始值为1
    brace_count = 1
    while brace_count > 0 and end_index < len(file_content):
        if file_content[end_index] == '{':
            brace_count += 1
        elif file_content[end_index] == '}':
            brace_count -= 1
        end_index += 1

        # 如果找到了闭合的大括号但计数器仍大于0，则继续搜索
        if brace_count == 0:
            break
    # 返回匹配的 lane 块的内容
    lane_info = file_content[start_index:end_index]
    #return file_content[start_index:end_index]
    return lane_info

def get_lane_id(lane_info):
    lane_id = re.findall(r'id: "(.*?)"', lane_info)
    return lane_id
def get_turn_info(lane_info):
    turn_info = re.findall(r'turn: (.*?)\n', lane_info)
    turn_info = [info.lower().replace('_', ' ') for info in turn_info]
    return turn_info
def insert_lane_marking(turn_info, lane_bound):
    if turn_info == 'no turn':
        line_marking = 'solid'
    elif turn_info == 'right turn':
        line_marking = 'dashed' if lane_bound == 'leftBound' else 'solid'
    elif turn_info == 'left turn':
        line_marking = 'solid' if lane_bound == 'leftBound' else 'dashed'
    elif turn_info == 'u turn':
        line_marking = 'dashed'
    else:
        line_marking = 'solid'  # default value
    return line_marking

def modify_boundary(boundary, points_pattern, line_marking_text, lane_match):
    process_boundary_points(boundary, lane_match.group('points'), points_pattern)
    line_marking = SubElement(boundary, 'lineMarking')
    line_marking.text = line_marking_text
def extract_predecessor_successor_ids(lane_id, lane_info):
    # 定义匹配predecessor_id和successor_id的正则表达式模式
    predecessor_pattern = re.compile(r'predecessor_id \{\s+id: "(?P<id>lane_\d+)"', re.DOTALL)
    successor_pattern = re.compile(r'successor_id \{\s+id: "(?P<id>lane_\d+)"', re.DOTALL)

    # 在lane_info中搜索所有的predecessor_id和successor_id
    predecessor_matches = predecessor_pattern.findall(lane_info)
    successor_matches = successor_pattern.findall(lane_info)
    # 初始化predecessor_ids和successor_ids列表
    predecessor_ids = []
    successor_ids = []

    # 遍历所有的predecessor_id，将它们添加到predecessor_ids列表中，并调用SubElement函数
    for match in predecessor_matches:
        predecessor_id = match.replace('lane_', '')
        predecessor_ids.append(predecessor_id)
        SubElement(lane_id, 'predecessor', ref=predecessor_id)

    # 遍历所有的successor_id，将它们添加到successor_ids列表中，并调用SubElement函数
    for match in successor_matches:
        successor_id = match.replace('lane_', '')
        successor_ids.append(successor_id)
        SubElement(lane_id, 'successor', ref=successor_id)

    # 返回predecessor_ids和successor_ids列表
    #return predecessor_ids, successor_ids

    left_neighbor_forward_pattern = re.compile(r'left_neighbor_forward_lane_id\s*{\s*id:\s*"(lane_\d+)"\s*}', re.DOTALL)
    right_neighbor_forward_pattern = re.compile(r'right_neighbor_forward_lane_id\s*{\s*id:\s*"(lane_\d+)"\s*}', re.DOTALL)
    left_neighbor_reverse_pattern = re.compile(r'left_neighbor_reverse_lane_id\s*{\s*id:\s*"(lane_\d+)"\s*}', re.DOTALL)
    right_neighbor_reverse_pattern = re.compile(r'right_neighbor_reverse_lane_id\s*{\s*id:\s*"(lane_\d+)"\s*}', re.DOTALL)
    # 在lane_info中搜索所有的right_neighbor_forward_lane_id,right_neighbor_reverse_lane_id,
    #left_neighbor_forward_lane_id,left_neighbor_reverse_lane_id
    left_neighbor_forward_matches = left_neighbor_forward_pattern.findall(lane_info)
    right_neighbor_forward_matches = right_neighbor_forward_pattern.findall(lane_info)
    left_neighbor_reverse_matches = left_neighbor_reverse_pattern.findall(lane_info)
    right_neighbor_reverse_matches = right_neighbor_reverse_pattern.findall(lane_info)
    right_neighbor_forward_ids = set()
    left_neighbor_reverse_ids = set()
    left_neighbor_forward_ids = set()
    right_neighbor_reverse_ids = set()

    # 创建一个Element对象

    #遍历所有的left_neighbor_forward_id，将它们添加到left_neighbor_forward_ids列表中，并调用SubElement函数

    #遍历所有的right_neighbor_forward_id，将它们添加到right_neighbor_forward_ids列表中，并调用SubElement函数
    for match in right_neighbor_forward_matches:
        right_neighbor_forward_id = match.replace('lane_', '')
        right_neighbor_forward_ids.add(right_neighbor_forward_id)
        SubElement(lane_id, 'adjacentRight', ref=right_neighbor_forward_id, drivingDir="same")

    # 遍历所有的left_neighbor_reverse_id，将它们添加到left_neighbor_reverse_ids列表中，并调用SubElement函数
    for match in left_neighbor_reverse_matches:
        left_neighbor_reverse_id = match.replace('lane_', '')
        left_neighbor_reverse_ids.add(left_neighbor_reverse_id)
        SubElement(lane_id, 'adjacentLeft', ref=left_neighbor_reverse_id, drivingDir="opposite")

    # 遍历所有的right_neighbor_reverse_id，将它们添加到right_neighbor_reverse_ids列表中，并调用SubElement函数
    for match in right_neighbor_reverse_matches:
        right_neighbor_reverse_id = match.replace('lane_', '')
        right_neighbor_reverse_ids.add(right_neighbor_reverse_id)
        SubElement(lane_id, 'adjacentRight', ref=right_neighbor_reverse_id, drivingDir="opposite")

    # 遍历所有的left_neighbor_forward_id，将它们添加到left_neighbor_forward_ids列表中，并调用SubElement函数
    for match in left_neighbor_forward_matches:
        left_neighbor_forward_id = match.replace('lane_', '')
        left_neighbor_forward_ids.add(left_neighbor_forward_id)
        SubElement(lane_id, 'adjacentLeft', ref=left_neighbor_forward_id, drivingDir="same")

    #print("ok")
    # 返回right_neighbor_forward_ids，left_neighbor_reverse_ids，right_neighbor_forward_ids和left_neighbor_reverse_ids列表
    #return list(right_neighbor_forward_ids), list(right_neighbor_reverse_ids), list(left_neighbor_forward_ids), list(left_neighbor_reverse_ids)


run_count = 0

def increment_run_count():     #函数运行计数器
    global run_count
    run_count += 1
    print(f"程序已运行 {run_count} 次")

def process_lane_points(root,data):
    print("ok")
    #points_pattern = re.compile(r'point \{\s+x: (?P<x>\d+\.\d+)\s+y: (?P<y>\d+\.\d+)\s+\}', re.DOTALL)
    points_pattern = re.compile(r'point \{\s+x: (?P<x>\d+(\.\d{1,6})?(?:\d*)?)\s+y: (?P<y>\d+(\.\d{1,6})?(?:\d*)?)\s+\}', re.DOTALL)
    # 处理左边界
    lane_pattern = re.compile(r'lane \{\s+id \{\s+id: "(?P<id>lane_\d+)"\s+\}.*?left_boundary \{.*?segment \{.*?line_segment \{(?P<points>(?:\s+point \{.*?\})+)\s+\}', re.DOTALL)
    # 处理左边界
    for lane_match in lane_pattern.finditer(data):
        lane_id = lane_match.group('id').replace('lane_', '')
        lane = SubElement(root, 'lanelet', id=lane_id)        
        left_boundary = SubElement(lane, 'leftBound')
        process_boundary_points(left_boundary, lane_match.group('points'), points_pattern)
        lane_info = extract_lane_by_id(data, lane_id)
        turn_info = get_turn_info(lane_info)
        line_marking_text = insert_lane_marking(turn_info, 'leftBound')
        line_marking = SubElement(left_boundary, 'lineMarking')
        line_marking.text = line_marking_text
    # 处理右边界
    lane_pattern = re.compile(r'lane \{\s+id \{\s+id: "(?P<id>lane_\d+)"\s+\}.*?right_boundary \{.*?segment \{.*?line_segment \{(?P<points>(?:\s+point \{.*?\})+)\s+\}', re.DOTALL)
    for lane_match in lane_pattern.finditer(data):
        lane_id = lane_match.group('id').replace('lane_', '')
        # 找到已经处理过的相应的lanelet
        lane = root.find(f"./lanelet[@id='{lane_id}']")
        if lane is not None:
            right_boundary = SubElement(lane, 'rightBound')
            process_boundary_points(right_boundary, lane_match.group('points'), points_pattern)
            lane_info = extract_lane_by_id(data, lane_id)
            turn_info = get_turn_info(lane_info)
            line_marking_text = insert_lane_marking(turn_info, 'leftBound')
            line_marking = SubElement(right_boundary, 'lineMarking')
            line_marking.text = line_marking_text        
            extract_predecessor_successor_ids(lane,lane_info)
        # 获取lane的其他属性
            increment_run_count()#调用函数运行计数器
            lane_type = re.search(r'type: (.*?)\n', data).group(1).lower().replace('_', ' ')
            if lane_type == 'city driving':
                lane_type = 'urban'
            SubElement(lane, 'laneletType').text = lane_type
#log:2023.04.13
#turn_info信息未提取成功，lane_marking_text未赋值成功



