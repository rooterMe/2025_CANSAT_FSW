import serial
import time

# Initialize serial port for EBIMU-9DOFV4
ser = serial.Serial(
    port='/dev/ttyAMA3',
    baudrate=115200,
    timeout=1
)

time.sleep(2)  # Wait for port to stabilize
print("Connecting to EBIMU-9DOFV4...")

# Example: Send initialization command to IMU
# Replace this command according to your device's manual
imu_init_cmd = "$VNWRG,07,40*5C\r\n"  # YPR output enable command with checksum
ser.write(imu_init_cmd.encode('ascii'))
print("IMU initialization command sent.")

# Start receiving data
try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore')
            print(line.strip())
except KeyboardInterrupt:
    print("Program terminated by user.")
    ser.close()
