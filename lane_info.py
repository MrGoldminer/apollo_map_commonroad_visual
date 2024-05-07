# def extract_all_lane_info():
#     # 打开源文件和目标文件
#     with open('./data/2.txt', 'r') as source, open('./data/3.txt', 'w') as target:
#         # 初始化括号计数器和lane块
#         brace_count = 0
#         lane_block = ''
#         lane_count = 0
#         # 逐行读取源文件内容
#         for line in source:
#             # 如果这一行包含无缩进的'lane {'，增加括号计数器
#             if line.strip().startswith('lane {'):
#                 brace_count += 1
#             # 如果括号计数器大于0，将这一行添加到lane块
#             if brace_count > 0:
#                 lane_block += line
#                 # 如果这一行包含'{'，增加括号计数器
#                 if '{' in line and not line.strip().startswith('lane {'):
#                     brace_count += 1
#                 # 如果这一行包含'}'，减少括号计数器
#                 if '}' in line:
#                     brace_count -= 1
#             # 如果括号计数器为0且lane块不为空，将lane块写入目标文件，然后清空lane块
#             if brace_count == 0 and lane_block.strip().startswith('lane {'):
#                 target.write(lane_block)
#                 lane_block = ''
#                 lane_count += 1
#                 print(f'Extracted {lane_count} lane blocks.')

#extract_all_lane_info()
import re
def is_in_range(x, y, x_range, y_range):
    x, y = float(x), float(y)
    return x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]

def extract_all_lane_info():
    points_pattern = re.compile(r'point \{\s+x: (?P<x>\d+(\.\d{1,6})?(?:\d*)?)\s+y: (?P<y>\d+(\.\d{1,6})?(?:\d*)?)\s+\}', re.DOTALL)
    x_range = [457300, 458400]
    y_range = [4400950, 4401490]

    with open('./data/2.txt', 'r') as source, open('./data/demo_base_map.txt', 'w') as target:
        brace_count = 0
        lane_block = ''
        lane_count = 0
        for line in source:
            if line.strip().startswith('lane {'):
                brace_count += 1
            if brace_count > 0:
                lane_block += line
                if '{' in line and not line.strip().startswith('lane {'):
                    brace_count += 1
                if '}' in line:
                    brace_count -= 1
            if brace_count == 0 and lane_block.strip().startswith('lane {'):
                # 在写入lane块之前，检查是否所有的点都在给定的范围内
                points_in_range = all(is_in_range(match.group('x'), match.group('y'), x_range, y_range) for match in points_pattern.finditer(lane_block))
                if points_in_range:
                    target.write(lane_block)
                    lane_count += 1
                    print(f'Extracted {lane_count} lane blocks.')
                lane_block = ''

extract_all_lane_info()
