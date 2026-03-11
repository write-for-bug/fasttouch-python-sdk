"""
Demo: End Effector Cartesian Servo Motion (set_end_effector_pose_euler_raw)
--------------------------------------------------------------------------
功能描述:
    本脚本演示如何使用 set_end_effector_pose_euler_raw 进行末端笛卡尔空间的实时伺服控制。
    示例动作：末端执行器在 Z 轴方向平滑地进行正弦往复运动。

核心 API 说明:
    - set_end_effector_pose_euler_raw(pos, euler):
        - pos: 目标位置 [x, y, z] (单位: m)。
        - euler: 目标欧拉角 [roll, pitch, yaw] (单位: rad)。
        - 特点：透传模式，无内部规划。必须以高频（通常 >= 100Hz）持续发送指令，
          且目标点之间的步进增量应尽量小，以保证运动平稳。

安全警告:
    1. 伺服模式下如果指令跳变过大，机械臂可能会产生剧烈抖动或触发保护。
    2. 确保计算出的目标点始终在机械臂的可达空间内。
"""

import time
import numpy as np
from fasttouch_python_sdk import FasttouchArm

# 1. 机械臂初始化
arm = FasttouchArm(can_port="can0")
print("Fasttouch SDK Initialized (EEF Servo Mode)")

try:
    # 2. 安全检查：先回到起始位姿，确保初始状态可控
    print("正在准备：先执行 go_home...")
    arm.go_home()
    time.sleep(3.5)

    # 3. 伺服运动参数设置
    freq = 0.4        # 频率: 0.4 Hz (2.5秒一个周期)
    amplitude = 0.05  # 往复幅值: 0.05 m (5厘米)
    hz = 100          # 循环控制频率: 100 Hz
    dt = 1.0 / hz
    duration = 10.0   # 持续时间: 10 秒

    # 获取当前末端位姿作为基准
    pos_start, euler_start = arm.get_ee_pose_euler()
    print(f"初始位姿: Pos={pos_start}, Euler={euler_start}")
    
    print(f"开始末端 Z 轴伺服运动... 持续 {duration} 秒")
    start_time = time.time()
    
    while (time.time() - start_time) < duration:
        t = time.time() - start_time
        
        # 4. 计算当前的目标位姿 (基于时间的正弦偏移)
        target_pos = pos_start.copy()
        target_pos[2] = pos_start[2] + amplitude * np.sin(2 * np.pi * freq * t)
        
        # 姿态保持不变
        target_euler = euler_start
        
        # 5. 调用伺服接口发送指令
        # 必须保证循环的频率足够稳定
        arm.set_end_effector_pose_euler_raw(pos=target_pos, euler=target_euler)
        
        time.sleep(dt)

    print("末端伺服运动结束")

except KeyboardInterrupt:
    print("\n用户中断运动")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    # 6. 必须释放资源
    arm.cleanup()
    print("Fasttouch 已释放")