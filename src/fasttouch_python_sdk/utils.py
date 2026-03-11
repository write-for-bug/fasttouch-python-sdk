import numpy as np
def quaternion_to_euler_wxyz(quat: np.ndarray) -> np.ndarray:
    """
    将四元数转换为欧拉角（roll, pitch, yaw）
    参数：
        quat: np.ndarray, 长度为 4 的数组 [w, x, y, z]
    返回：
        roll, pitch, yaw: 以弧度为单位的欧拉角
    """
    w, x, y, z = quat
    # 计算 roll (x 轴旋转)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    # 计算 pitch (y 轴旋转)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = np.pi / 2 * np.sign(sinp)  # 使用 90 度限制
    else:
        pitch = np.arcsin(sinp)

    # 计算 yaw (z 轴旋转)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return np.array([roll, pitch, yaw])


def quaternion_to_euler_xyzw(q: np.ndarray) -> np.ndarray:
    """
    将四元数转换为欧拉角 (ZYX顺序，通常用于机械臂)
    输入: q = [qx, qy, qz, qw] 或 [w, x, y, z]
    输出: [rx, ry, rz] (弧度)
    """
    if len(q) == 4:
        # 根据您的数据，看起来是[qx, qy, qz, qw]格式
        x, y, z, w = q[0], q[1], q[2], q[3]
    else:
        raise ValueError("四元数必须是4维向量")
    
    # 转换为欧拉角 (ZYX顺序，即先绕Z轴，再绕Y轴，最后绕X轴)
    # roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)
    
    # pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = np.copysign(np.pi / 2, sinp)  # 使用90度
    else:
        pitch = np.arcsin(sinp)
    
    # yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)
    
    return np.array([roll, pitch, yaw])  # [rx, ry, rz]


def euler_to_quaternion(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """
    将欧拉角（roll, pitch, yaw）转换为四元数。

    参数：
        roll: 绕 x 轴的旋转角（弧度）
        pitch: 绕 y 轴的旋转角（弧度）
        yaw: 绕 z 轴的旋转角（弧度）

    返回：
        np.ndarray: 长度为 4 的四元数数组 [w, x, y, z]
    """
    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return np.array([w, x, y, z])
