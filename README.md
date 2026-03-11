# Fasttouch Python SDK

Fasttouch 机械臂的 Python SDK，通过 CAN 总线与机械臂通信，提供关节控制、末端位姿控制和夹爪操作功能。

## 硬件要求

- Fasttouch 机械臂
- CAN 接口适配器（如 USB-CAN）
- Linux 系统（推荐 Ubuntu 22.04 / 20.04）

## 前置准备

### 1. 克隆仓库

```bash
git clone https://github.com/write-for-bug/fasttouch-python-sdk.git
cd fasttouch-python-sdk
```

### 2. 创建 Conda 环境

```bash
conda create -n fasttouch python=3.10
conda activate fasttouch
```

### 3. 安装 CAN 工具以及相关依赖

```bash
sudo apt-get install can-utils
sudo apt-get install liborocos-kdl-dev
sudo apt-get install pybind11-dev
```

### 4. 安装 SDK

```bash
# 普通安装
pip install .

# 或可编辑模式安装（便于修改源码）
pip install -e .
```
### 2. 激活 CAN 接口

使用机械臂前必须先激活 CAN 接口：

**单臂：**
```bash
sudo ip link set can0 up type can bitrate 1000000
```

**多臂：**
```bash
sudo ip link set can0 up type can bitrate 1000000
sudo ip link set can1 up type can bitrate 1000000
```

不同机械臂使用不同的 CAN 接口（can0, can1, can2...），在初始化时通过 `can_port` 参数指定。

⚠️can口是热插拔的，can0 can1设定顺序与插拔顺序有关

## 快速开始

```python
import time
from fasttouch_python_sdk import FasttouchArm

# 1. 初始化机械臂
arm = FasttouchArm(can_port="can0")

try:
    # 2. 回到归位点
    arm.go_home()
    time.sleep(3.5)  # 等待运动完成
    
    # 3. 移动到目标关节角度 (单位: 弧度)
    arm.set_joint(positions=[0.2,0.0, 0.4, 0.0, 0.5, 0.0], tf=3.0)
    time.sleep(3.5)
    
    # 4. 获取当前位置
    positions = arm.get_joint_positions()
    print(f"当前关节角度: {positions}")
    
    # 5. 控制夹爪 (0.0 = 闭合, 1.0 = 全开)
    arm.openGripper()  # 或 closeGripper()
    
finally:
    # 6. 释放资源 (必须调用!)
    arm.cleanup()
```

## API 参考

### 初始化

```python
arm = FasttouchArm(can_port="can0")  # can_port 默认为 "can0"
```

### 运动控制

| 方法 | 描述 |
|------|------|
| `go_home()` | 移动到归位点 |
| `set_joint(positions, tf, ctrl_hz)` | 关节空间规划运动 |
| `set_joint_raw(positions, velocities)` | 关节伺服透传（无规划） |
| `set_end_effector_pose_euler(pos, euler, tf)` | 末端位姿控制（欧拉角） |
| `set_end_effector_pose_quat(pos, quat, tf)` | 末端位姿控制（四元数） |

**参数说明：**
- `positions`: 目标关节角度列表，长度 6，单位弧度
- `tf`: 运动时间（秒）
- `ctrl_hz`: 控制频率，默认 400Hz
- `pos`: 末端位置 [x, y, z]，单位米
- `euler`: 欧拉角 [roll, pitch, yaw]，单位弧度
- `quat`: 四元数 [w, x, y, z]

### 状态读取

| 方法 | 描述 |
|------|------|
| `get_joint_positions()` | 获取关节角度 (np.ndarray, 6) |
| `get_joint_velocities()` | 获取关节速度 (np.ndarray, 6) |
| `get_joint_torques()` | 获取关节力矩 (np.ndarray, 6) |
| `get_ee_pose_euler()` | 获取末端位姿 (位置, 欧拉角) |
| `get_ee_pose_quat()` | 获取末端位姿 (位置, 四元数) |

### 夹爪控制

| 方法 | 描述 |
|------|------|
| `openGripper()` | 打开夹爪 |
| `closeGripper()` | 关闭夹爪 |
| `setGripperPosition(position)` | 带规划的夹爪位置控制 |
| `setGripperPosition_raw(position)` | 透传夹爪位置控制 (0.0-1.0) |
| `get_gripper_position()` | 获取夹爪当前位置 |

### 资源释放

```python
arm.cleanup()  # 必须在程序结束时调用，释放 CAN 资源
```

## 运动模式说明

### 规划运动 vs 透传运动

SDK 提供两种控制模式：

1. **规划运动**（如 `set_joint`, `set_end_effector_pose_euler`）
   - 包含时间参数 `tf`
   - 使用多项式插值生成平滑轨迹
   - 适合点位移动

2. **透传运动**（如 `set_joint_raw`, `set_end_effector_pose_euler_raw`）
   - 无时间规划
   - 指令直接下发
   - 适合伺服控制

## 示例脚本

`demo/` 目录下包含多个示例：

| 文件 | 功能 |
|------|------|
| `00_init.py` | 初始化与归位 |
| `02_movj.py` | 关节空间运动 |
| `03_servoj.py` | 关节伺服控制 |
| `04_movp.py` | 末端位姿控制 |
| `05_servop.py` | 末端伺服控制 |
| `06_gripper_ctrl.py` | 夹爪控制 |

运行示例：
```bash
python demo/02_movj.py
```

## 注意事项

1. **必须激活 CAN**：使用前执行 `sudo ip link set can0 up type can bitrate 1000000`（多臂则依次激活 can0, can1 等）
2. **清理资源**：程序结束前必须调用 `arm.cleanup()` 释放 CAN 接口
3. **运动安全**：确保机械臂工作范围内无障碍物
4. **夹爪安全**：闭合夹爪时确保无手指或物品在夹爪行程内
