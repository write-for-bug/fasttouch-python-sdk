"""
Demo: End Effector Cartesian Motion (set_end_effector_pose_euler)
---------------------------------------------------------------
功能描述:
    本脚本演示如何获取机械臂末端执行器（EEF）的当前位姿，并进行相对位置控制。
    具体动作：读取当前位姿 -> 向上移动 10cm -> 回到原位 -> 往复执行。

核心 API 说明:
    - get_ee_pose_euler(): 
        - 返回当前末端在基坐标系下的位置 (x, y, z) 和欧拉角 (roll, pitch, yaw)。
    - set_end_effector_pose_euler(pos, euler, tf):
        - pos: 目标笛卡尔位置列表 [x, y, z] (单位: m)。
        - euler: 目标欧拉角列表 [r, p, y] (单位: rad)。
        - tf: 运动完成所需的时间 (单位: 秒)。
        - 该方法内部包含逆解计算与平滑轨迹规划。

安全警告:
    1. 向上移动 10cm 前，请确保机械臂上方无障碍物，且不会达到关节限位。
    2. 笛卡尔运动涉及逆解，请确保目标点在机械臂的可达工作空间内。
"""

import time
import numpy as np
from fasttouch_python_sdk import FasttouchArm

# 1. 机械臂初始化
arm = FasttouchArm(can_port="can0")
print("Fasttouch SDK Initialized")

try:
    # 2. 安全检查：先回到起始位姿
    print("正在执行 go_home...")
    arm.go_home()
    time.sleep(3.5)

    # 3. 读取初始末端位姿作为基准
    # pos_start: [x, y, z], euler_start: [r, p, y]
    pos_start, euler_start = arm.get_ee_pose_euler()
    print(f"初始末端位置: {pos_start}")
    print(f"初始末端姿态: {euler_start}")

    # 定义往复运动次数
    loops = 3
    offset_z = 0.1  # 向上移动 10cm (0.1米)

    for i in range(loops):
        print(f"\n--- 第 {i+1} 次往复运动 ---")

        # 4. 向上运动
        target_pos_up = pos_start.copy()
        target_pos_up[2] += offset_z  # Z 轴增加 10cm
        
        print(f"动作：向上移动 {offset_z*100} cm...")
        arm.set_end_effector_pose_euler(pos=target_pos_up, euler=euler_start, tf=2.0)
        time.sleep(2.5) # 等待运动完成

        # 5. 回到原位
        print("动作：回到初始位置...")
        arm.set_end_effector_pose_euler(pos=pos_start, euler=euler_start, tf=2.0)
        time.sleep(2.5)

    print("\n往复运动任务完成")

except KeyboardInterrupt:
    print("\n用户中断运动")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    # 6. 必须释放资源
    arm.cleanup()
    print("Fasttouch 已释放")