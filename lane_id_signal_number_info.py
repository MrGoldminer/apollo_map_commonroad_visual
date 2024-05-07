import re
from xml.etree.ElementTree import SubElement
def extract_lane_by_id(data, lane_id):
    data = './data/3.txt'
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
    
    return file_content[start_index:end_index]

# 使用示例
data = './data/3.txt'
lane_id = 4995123454776
lane_info = extract_lane_by_id(data, lane_id)
#print(lane_info)
with open('lane_id_5743.txt', 'w') as f:
    f.write(str(lane_info))


# predecessor_ids, successor_ids = extract_predecessor_successor_ids(lane_id, lane_info)
# print("Lane ID:", lane_id)
# print("Predecessor IDs:", predecessor_ids)
# print("Successor IDs:", successor_ids)
