# file: send_IMU_via_BT.py

import serial
import time

IMU_PORT = '/dev/ttyAMA3'
BT_PORT = '/dev/ttyS0'

IMU_serial = serial.Serial(IMU_PORT, baudrate=921600, timeout=0.001)
BT_serial = serial.Serial(BT_PORT, baudrate=921600, timeout=0.001)

def get_IMU_data():
    IMU_serial.write(b'*')
    buffer = ""
    while True:
        if IMU_serial.in_waiting:
            data = IMU_serial.read()
            if data not in [b'\r', b'\n']:
                buffer += data.decode(errors='ignore')
            elif data == b'\n' and len(buffer) > 0:
                return buffer.strip()

def send_BT_data(data):
    BT_serial.write(data.encode())
    BT_serial.write(b'\r\n')  
    
def main():
    if not IMU_serial.is_open or not BT_serial.is_open:
        print("seiral x")
        return

    print("serial o")

    while True:
        try:
            imu_data = get_IMU_data()
            print(f"IMU: {imu_data}")
            send_BT_data(imu_data)
        except Exception as e:
            print(f"error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
