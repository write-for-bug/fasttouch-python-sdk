from fasttouch_python_sdk import FasttouchArm

arm = FasttouchArm(can_port="can0")
print("fasttouch initialized")
try:
    arm.go_home()
    print("fasttouch go home")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    arm.cleanup()
    print("fasttouch released")