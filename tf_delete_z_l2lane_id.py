# import re

# def rewrite_lane_id():
#     # 打开源文件和目标文件
#     with open('base_map.txt', 'r') as source, open('new_yizhuang_base_map.txt', 'w') as target:
#         # 读取源文件内容
#         content = source.read()
#         # 定义匹配模式
#         pattern = re.compile(r'(id:\s*"l_(\d+)_?(\d*)")')
#         # 找到所有匹配的字符串并替换
#         new_content = pattern.sub(lambda m: 'id: "lane_{}{}"'.format(m.group(2), '001'+m.group(3) if m.group(3) else ''), content)
#         # 将新内容写入目标文件
#         target.write(new_content)

# rewrite_lane_id()
#对齐lane_id的代码，将l_1_1转换为lane_1001，l_1_2转换为lane_1002，以此类推。
import re

def rewrite_lane_id():
    # 打开源文件和目标文件
    with open('./data/base_map.txt', 'r') as source, open('./data/2.txt', 'w') as target:
        # 读取源文件内容
        content = source.read()
        # 定义匹配模式
        pattern = re.compile(r'(id:\s*"l_(\d+)_?(\d*)")')
        # 找到所有匹配的字符串并替换
        #new_content = pattern.sub(lambda m: 'id: "lane_{}{}"'.format(m.group(2), m.group(3) if m.group(3) else ''), content)
        new_content = pattern.sub(lambda m: 'id: "lane_{}{}"'.format(m.group(2), '12345'+m.group(3) if m.group(3) else ''), content)
        # 删除所有的'z: num'行
        new_content = re.sub(r'\s*z:.*', '', new_content)
        # 将新内容写入目标文件
        target.write(new_content)

rewrite_lane_id()
##对齐lane_id的代码，将l_1_1转换为lane_11，l_1_2转换为lane_112，以此类推；删除所有的'z: num'行

