from typing import List, Tuple, Union, Optional, Dict, Any
import numpy as np
import os
from . import fasttouch_python_sdk as _ext
from .utils import quaternion_to_euler_wxyz,quaternion_to_euler_xyzw,euler_to_quaternion
# try:
#     from . import fasttouch_python_sdk as _ext
# except ImportError as e:
#     raise ImportError(
#         f"Failed to load Startouch C++ extension: {e}. "
#         "Please run: pip install startouch-python-sdk"
#     ) from e


class FasttouchArm:
    """
    Base class for a single robot arm.

    Args:
        config (Dict[str, sAny]): Configuration dictionary for the robot arm

    Attributes:
        config (Dict[str, Any]): Configuration dictionary for the robot arm
        num_joints (int): Number of joints in the arm
    """

    def __init__(self,can_port = "can0"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        permutation_matrix = os.path.join(current_dir, 'param_csv_gripper', 'permutationMatrix.csv')
        pi_b = os.path.join(current_dir, 'param_csv_gripper', 'pi_b.csv')
        pi_fr = os.path.join(current_dir, 'param_csv_gripper', 'pi_fr.csv')
        
        self.arm = _ext.ArmController(can_interface = can_port,enable_fd = False,gripper_exist  =True,
                                           permutation_matrix=permutation_matrix,pi_b =pi_b,pi_fr = pi_fr)


    def go_home(self) -> bool:
        """
        Move the robot arm to a pre-defined home pose.

        Returns:
            bool: True if the action was successful, False otherwise
        """
        q_start = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 设置回到起点的位姿
        self.arm.set_joint(q_start, tf=3.0)
        return True

    def gravity_compensation(self) -> bool:
        self.arm.gravity_compensation()  
        return True


    # 带时间规划
    def set_joint(
        self,
        positions: Union[List[float], np.ndarray],  # Shape: (num_joints, 单位rad)
        tf: float = 2.0,  # 默认时间：4.0秒
        ctrl_hz: float = 400.0,  # 默认控制频率：300.0Hz
    ) -> bool:
        """
        Move the arm to the given joint position(s).

        Args:
            positions: Desired joint position(s). Shape: (6)
            **kwargs: Additional arguments
        带有时间规划的多项式

        """
        self.arm.set_joint(q_end = positions,tf = tf, ctrl_hz = ctrl_hz)
        return True

    # 关节伺服
    def set_joint_raw(
        self,
        positions: Union[List[float], np.ndarray],  # Shape: (num_joints,单位rad)
        velocities: Union[List[float], np.ndarray],  # Shape: (num_joints,)
    ) -> bool:
        """
        Move the arm to the given joint position.

        Args:
            positions: Desired joint position(s). Shape: (6)
            **kwargs: Additional arguments
        角度透传 没有规划！！ 谨慎使用

        """
        self.arm.set_joint_raw(q_end = positions,v_end = velocities)
        return True


    # 带时间规划
    def set_end_effector_pose_euler(
        self,
        pos: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (3,)
        euler: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (3,)
        tf: float = 2.0,  # 默认时间：4.0秒 但位置速度控制模式和linear插值模式下不生效
    ) -> bool:
        """
        /**
        * @brief 设置末端执行器的目标位姿
        * 
        * 此函数用于设置末端执行器的目标位置和姿态。目标位置由三维向量 `target_pos` 指定，
        * 目标姿态通过欧拉角 `target_euler` 给出。`tf` 参数定义了到达目标位姿的时间，默认为 4.0 秒。
        *
        * @param target_pos 目标位置，三维向量 (x, y, z)
        * @param target_euler 目标姿态，欧拉角 (roll, pitch, yaw)
        * @param tf 目标位姿的到达时间，单位为秒，默认值为 4.0
        */
        """
        self.arm.set_end_effector_pose(target_pos=pos, target_euler=euler, tf=tf)
        return True
    
    def set_end_effector_pose_euler_raw(
        self,
        pos: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (3,)
        euler: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (3,)
    ) -> bool:
        """
        /**
        * @brief 设置末端执行器的目标位姿
        * 
        * 此函数用于设置末端执行器的目标位置和姿态。目标位置由三维向量 `target_pos` 指定，
        * 目标姿态通过欧拉角 `target_euler` 给出。`tf` 参数定义了到达目标位姿的时间，默认为 4.0 秒。
        *
        * @param target_pos 目标位置，三维向量 (x, y, z)
        * @param target_euler 目标姿态，欧拉角 (roll, pitch, yaw)
        */
        """
        self.arm.set_end_effector_pose_raw(target_pos=pos, target_euler=euler)
        return True
    
    # 带时间规划
    def set_end_effector_pose_quat(
        self,
        pos: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (3,)
        quat: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (4,)
        tf: float = 2.0,  # 
    ) -> bool:
        euler = quaternion_to_euler_wxyz(quat)
        self.arm.set_end_effector_pose(target_pos=pos, target_euler=euler, tf=tf)
        return True



    # 透传、适合伺服控制
    def set_end_effector_pose_quat_raw(
        self,
        pos: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (3,)
        quat: Optional[Union[List[float], np.ndarray]] = None,  # Shape: (4,)
    ) -> bool:
        euler = quaternion_to_euler_wxyz(quat)  
        self.arm.set_end_effector_pose_raw(target_pos=pos, target_euler=euler)
        return True
    




    def get_joint_positions(self) -> np.ndarray:
        """
        Get the current joint position(s) of the arm.

        Args:
            joint_names: Name(s) of the joint(s) to get positions for. Shape: (num_joints,) or single string. If None,
                            return positions for all joints.

        """
        return self.arm.get_joint_positions()

    def get_joint_velocities(self) -> np.ndarray:
        """
        Get the current joint velocity(ies) of the arm.

        """
        return self.arm.get_joint_velocities()

    def get_joint_torques(self) -> np.ndarray:
        """
        Get the current joint torque(s) of the arm.        """
        return self.arm.get_joint_torques()
    

    def get_ee_pose_quat(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get the current end effector pose of the arm.

        Returns:
            End effector pose as (position, quaternion)
            Shapes: position (3,), quaternion (4,) [w, x, y, z]
        """
        result = self.arm.get_end_effector_pose()
        pos_t = result[0]#类型np.ndarray
        rpy_t = result[1]
        quat = euler_to_quaternion(rpy_t[0], rpy_t[1], rpy_t[2])
        # 返回位置和四元数
        return pos_t,quat

    def get_ee_pose_euler(
        self,
    ) -> Tuple[np.ndarray, np.ndarray]:

        result = self.arm.get_end_effector_pose()
        pos_t = result[0]#类型np.ndarray
        rpy_t = result[1]
        return pos_t,rpy_t
    

    def openGripper(self) -> bool:
        #把夹爪开到最大
        self.arm.openGripper()
        return True


    def closeGripper(self) -> bool:
        #把夹爪闭合
        self.arm.closeGripper()
        return True

    def setGripperPosition_raw(self, position:float) -> bool:
        #角度透传模式   不规划
        #设置夹爪开合程度  0是闭合 1是开合
        self.arm.setGripperPosition_raw(position)
        return True
    
    def setGripperPosition(self, position:float) -> bool:
        #设置夹爪开合程度  0是闭合 1是开合  #设置0时有点问题，有提示
        self.arm.setGripperPosition(position)
        return True


    def get_gripper_position(self) -> float:
        #设置夹爪开合程度  0是闭合 1是开合
        return self.arm.get_gripper_position()


    def cleanup(self):
        self.arm.cleanup()
