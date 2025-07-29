import serial
import time

# EBIMU �ʱ� �ӵ��� ���� ��Ʈ ���� (921600bps)
ser = serial.Serial(
    port='/dev/ttyAMA3',
    baudrate=921600,
    timeout=1
)

print("Sending <sb5> to set 115200bps...")
ser.write(b'<sod1>')
time.sleep(0.5)  # IMU ���� ���

# ���� �б�
resp = ser.read(ser.in_waiting or 1).decode('ascii', errors='ignore')
print("Response:", resp.strip())

ser.close()