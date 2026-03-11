"""
Demo: Real-time Status Monitoring (read_status)
----------------------------------------------
功能描述:
    本脚本演示如何实时获取并监控 FasttouchArm 机械臂的各项物理状态数据。
    它涵盖了从底层关节空间到末端笛卡尔空间的全面数据读取，适用于调试、示教记录或状态可视化。

核心 API 说明:
    - get_joint_positions(): 获取当前各关节的旋转角度 (单位: rad)。
    - get_joint_torques(): 获取当前各关节感知的实时力矩 (单位: N·m)。
    - get_ee_pose_euler(): 获取末端执行器（TCP）在基坐标系下的位置 (m) 与欧拉角姿态 (rad)。
    - get_gripper_position(): 获取当前夹爪的开合程度 (0 为闭合，1 为全开)。

环境与安全要求:
    1. 确保已通过终端配置好 CAN 接口速率（通常为 1M 或 500K）。
    2. 脚本运行之初会执行 go_home()，请确保机械臂周围无遮挡。
    3. 退出使用 Ctrl+C，以触发 finally 块中的 cleanup() 释放 CAN 总线占用。
    4. 确保 Linux 系统已正确初始化 CAN 驱动 (sudo ip link set can0 up type can bitrate 1000000)。
"""
import time
import numpy as np
import os
from fasttouch_python_sdk import FasttouchArm

# 1. 初始化
arm = FasttouchArm(can_port="can0")
print("--- Fasttouch Arm 实时状态监控 (按 Ctrl+C 退出) ---")

# 先回原点
arm.go_home()
# time.sleep(1) # 等待动作启动

try:
    while True:
        # 2. 读取数据
        joint_pos = arm.get_joint_positions()
        joint_torque = arm.get_joint_torques()
        pos_e, euler_e = arm.get_ee_pose_euler()
        gripper_pos = arm.get_gripper_position()

        # 3. 格式化输出 
        output = (
            f"\n\n[JONIT] " + " ".join([f"J{i}:{p:7.4f}" for i,p in enumerate(joint_pos)]) + 
            f"\n[XYZ] " + " ".join([f"{x:7.4f}" for x in pos_e]) +
            f"\n[RPY] " + " ".join([f"{x:7.4f}" for x in euler_e]) +
            f"\n[TORQUE] " + " ".join([f"{x:7.4f}" for x in joint_torque]) +
            f"\n[GRIPPER] {gripper_pos:.3f}"
        )
        
       
        print(output, end="", flush=True)

        # 4. 控制循环频率 (例如 50Hz)
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\n\n检测到用户中断，正在停止...")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    # 5. 释放资源
    arm.cleanup()
    print("Arm released")