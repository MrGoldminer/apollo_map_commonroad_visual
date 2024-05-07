1.输入文件名为："base_map.txt"
2.运行命令："python main.py"
3.注意检查各路径文件输入输出名称正确
4."base_map.txt"是有apollo docker环境里面运行：

    source scripts/apollo_base.sh
    protoc --decode apollo.hdmap.Map modules/map/proto/map.proto < modules/map/data/sunnyvale_loop/base_map.bin > base_map.txt 
#低版本命令，暂未验证
    protoc --decode apollo.hdmap.Map modules/common_msgs/map_msgs/map.proto < modules/map/data/borregas_ave/base_map.bin > base_map.txt 
#apollo9.0环境测试成功
#https://github.com/daohu527/Apollo-1000-questions/blob/main/questions/how_to_change_base_map_to_human_readable.md
#apollo使用参考"/tool/apollo使用命令.txt"

resources:/home/goldminer/maptfosm/yizhaung_quanliucheng二维适配/Basemap_tf_txt.docx

5.如果在可视化地图的时候，出现报错，可以运行："maptfosm/yizhaung_quanliucheng二维适配/tool/lane_info/lane_id_signal_number_info.py"这个命令查看其lane_info具体信息

同时，可暂时将其id加入5.csv文件中，重新运行命令："python main.py"，即可

6.对于/home/goldminer/maptfosm/yizhaung_quanliucheng二维适配/find_left_right_point_different.py，可以检查其左右point个数不一致的id
7.对于/home/goldminer/maptfosm/yizhaung_quanliucheng二维适配/fix_left_right_differenr.py使修复这个问题的代码，具体可以进一步优化
