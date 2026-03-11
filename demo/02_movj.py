"""
Demo: Joint Space Motion (movj)
---------------------------------------
功能描述:
    本脚本演示如何使用 FasttouchArm SDK 进行关节空间的规划运动（movj）。
    通过 set_joint 方法，机械臂将根据指定的时间（tf）利用内部的多项式插值算法，
    平滑地从当前位姿移动到目标关节位姿。

核心 API 说明:
    - FasttouchArm(can_port): 初始化机械臂，自动加载模型参数与 CAN 接口。
    - go_home(): 将机械臂移动至预设的零位起点。
    - set_joint(positions, tf, ctrl_hz): 
        - positions: 目标关节角度列表 (单位: rad)。
        - tf: 到达目标位姿所需的时间 (单位: 秒)。
        - ctrl_hz: 内部规划器的控制频率，默认 400Hz。
    - cleanup(): 停止控制器并关闭 CAN 通讯，是安全退出的必要步骤。

安全警告:
    1. 运行前请确保机械臂工作范围内无障碍物。
    2. 确保 Linux 系统已正确初始化 CAN 驱动 (sudo ip link set can0 up type can bitrate 1000000)。
"""

import time
import numpy as np
from fasttouch_python_sdk import FasttouchArm

# 1. 机械臂初始化
# 构造函数会加载内部所需的 CSV 配置文件并建立底层控制连接
arm = FasttouchArm(can_port="can0")
print("Fasttouch SDK Initialized")

try:
    # 2. 安全检查：回到起始位姿
    # go_home 内部同样带有时间规划，确保启动平稳
    print("正在执行 go_home...")
    arm.go_home()
    time.sleep(3.5) # 等待规划运动完成

    # 3. 关节空间规划运动 (movj)
    # 目标关节角 (rad)
    target_joints = [0.2, -0.3, 0.4, 0.0, 0.5, 0.0]
    
    print(f"开始 movj 运动，目标位姿: {target_joints}")
    # 调用带规划的 set_joint 方法
    arm.set_joint(positions=target_joints, tf=3.0, ctrl_hz=400.0)
    
    # 等待运动完成 (tf + buffer 冗余时间)
    time.sleep(3.5)
    
    # 4. 读取当前位置进行验证
    current_q = arm.get_joint_positions()
    print(f"运动完成，当前关节角度: {current_q.round(4)}")

except KeyboardInterrupt:
    print("\n用户中断运动")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    # 5. 必须释放资源
    # 显式调用 cleanup 以释放 CAN 接口，防止后续程序无法连接
    arm.cleanup()
    print("Fasttouch 已释放")
import time
import numpy as np
from fasttouch_python_sdk import FasttouchArm

# 1. 机械臂初始化
arm = FasttouchArm(can_port="can0")
print("Fasttouch SDK Initialized")

try:
    # 2. 回到起始位姿 (通常作为运动前的安全检查)
    print("正在执行 go_home...")
    arm.go_home()
    time.sleep(3.5) # 等待规划运动完成

    # 3. 关节空间规划运动 (movj)
    # set_joint 使用多项式插值进行平滑规划
    # positions: 目标关节角 (rad)
    # tf: 到达时间 (秒)
    # ctrl_hz: 控制频率 (Hz)
    target_joints = [0.2, -0.3, 0.4, 0.0, 0.5, 0.0]
    
    print(f"开始 movj 运动，目标位姿: {target_joints}")
    arm.set_joint(positions=target_joints, tf=3.0, ctrl_hz=400.0)
    
    # 等待运动完成 (tf + buffer)
    time.sleep(3.5)
    
    # 4. 读取当前位置验证
    current_q = arm.get_joint_positions()
    print(f"运动完成，当前关节角度: {current_q.round(4)}")

except KeyboardInterrupt:
    print("\n用户中断运动")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    # 5. 必须释放资源
    # 否则 CAN 通道可能被占用导致下次无法启动
    arm.cleanup()
    print("Fasttouch 已释放")