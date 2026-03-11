"""
Demo: Joint Space Servo Motion (set_joint_raw)
---------------------------------------
功能描述:
    本脚本演示如何使用 set_joint_raw 方法进行关节空间的实时伺服控制。
    示例中让关节 1 (J1) 以正弦波曲线进行往复运动。

核心 API 说明:
    - set_joint_raw(positions, velocities): 
        - positions: 目标关节位置列表 (rad)。
        - velocities: 目标关节速度列表 (rad/s)。
        - 注意：该接口为透传模式，不带内部轨迹规划。必须以高频（通常 >= 100Hz）
          持续发送指令，否则机械臂运动会出现卡顿。

安全警告:
    1. 伺服模式下指令直接作用于底层，请确保计算出的增量极小。
    2. 建议先在低幅值下或debug模式下测试，确保逻辑正确。
"""

import time
import numpy as np
from fasttouch_python_sdk import FasttouchArm

# 1. 机械臂初始化
arm = FasttouchArm(can_port="can0")
print("Fasttouch SDK Initialized (Servo Mode)")

try:
    # 2. 安全起见：先回原点，确保初始状态可控
    print("正在准备：先执行 go_home...")
    arm.go_home()
    time.sleep(3.5)

    # 3. 正弦运动参数设置
    freq = 0.5        # 频率: 0.5 Hz (2秒一个周期)
    amplitude = 0.3   # 幅值: 0.3 rad (约 17 度)
    hz = 100          # 循环控制频率: 100 Hz
    dt = 1.0 / hz     # 步长时间
    duration = 10.0   # 运行总时长: 10 秒

    # 获取当前基准位姿
    q_start = arm.get_joint_positions()
    
    print(f"开始正弦运动 (J1)... 持续 {duration} 秒")
    start_time = time.time()
    
    while (time.time() - start_time) < duration:
        t = time.time() - start_time
        
        # 计算当前目标位置 (基于正弦函数)
        # 仅修改关节 1，其余关节保持原位
        target_q = q_start.copy()
        target_q[0] = q_start[0] + amplitude * np.sin(2 * np.pi * freq * t)
        
        # 计算当前目标速度 (位置的导数)
        target_v = np.zeros(6)
        target_v[0] = amplitude * (2 * np.pi * freq) * np.cos(2 * np.pi * freq * t)
        
        # 4. 调用透传接口发送指令
        # positions 必须提供完整列表，velocities 用于前馈控制提高精度
        arm.set_joint_raw(positions=target_q, velocities=target_v)
        
        # 控制循环频率在 100Hz 左右
        time.sleep(dt)

    print("正弦运动结束")

except KeyboardInterrupt:
    print("\n用户中断运动")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    # 5. 必须释放资源
    arm.cleanup()
    print("Fasttouch 已释放")