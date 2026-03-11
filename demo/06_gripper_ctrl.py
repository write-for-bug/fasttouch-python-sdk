"""
Demo: Gripper Control (Open/Close & Servo Raw)
---------------------------------------------
功能描述:
    本脚本演示如何控制 FasttouchArm 的末端夹爪。
    包含：基础的全开/全关动作，以及使用 setGripperPosition_raw 进行实时位姿伺服。

核心 API 说明:
    - openGripper(): 将夹爪快速开启至最大位置。
    - closeGripper(): 将夹爪快速闭合。
    - setGripperPosition_raw(position):
        - position: 夹爪开合程度，范围 0.0 ~ 1.0 (0为闭合，1为全开)。
        - 特点：透传模式，无内部规划，指令直接下发。

安全警告:
    1. 闭合夹爪前，请确保手指或物品不在夹爪行程内，避免夹伤。
    2. 频繁的高频伺服指令（raw）应保持数值平滑，避免夹爪电机剧烈震动。
"""

import time
import numpy as np
from fasttouch_python_sdk import FasttouchArm

# 1. 机械臂初始化
arm = FasttouchArm(can_port="can0")
print("Fasttouch SDK Initialized (Gripper Demo)")

try:
    # 2. 基础开合动作演示
    print("\n--- 基础动作演示 ---")
    
    print("动作：开启夹爪...")
    arm.openGripper()
    time.sleep(1.5)
    
    print("动作：闭合夹爪...")
    arm.closeGripper()
    time.sleep(1.5)

    # 3. 伺服透传模式演示 (setGripperPosition_raw)
    print("\n--- 伺服透传演示 (0.0 -> 1.0 -> 0.0) ---")
    
    # 模拟一个缓慢张开再闭合的过程
    steps = 100
    
    # 缓慢张开
    print("正在平滑张开...")
    for i in range(steps + 1):
        pos = i / steps  # 从 0.0 渐变到 1.0
        arm.setGripperPosition_raw(pos)
        time.sleep(0.02) # 50Hz 更新频率
        
    time.sleep(0.5)
    
    # 缓慢闭合
    print("正在平滑闭合...")
    for i in range(steps, -1, -1):
        pos = i / steps  # 从 1.0 渐变到 0.0
        arm.setGripperPosition_raw(pos)
        time.sleep(0.02)

    # 4. 读取当前夹爪位置验证
    # 注意：get_gripper_position 获取的是当前的反馈位置
    final_pos = arm.get_gripper_position()
    print(f"\n当前夹爪最终位置反馈: {final_pos:.3f}")

except KeyboardInterrupt:
    print("\n用户中断程序")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    # 5. 释放资源
    arm.cleanup()
    print("Fasttouch 已释放")