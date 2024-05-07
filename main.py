import subprocess
import os
subprocess.call(["python", "tf_delete_z_l2lane_id.py"])
subprocess.call(["python", "lane_info.py"])
subprocess.call(["python", "base2sind.py"])
subprocess.call(["python", "v109fix_left_right_differenr.py"])
#subprocess.call(["python", "twice_fix_left_right_differenr.py"])
subprocess.call(["python", "visual-10.py"])
