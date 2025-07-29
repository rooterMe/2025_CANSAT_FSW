# file: bt_time_test_using_can_BT.py

import time
import serial

# Initialize Bluetooth serial object
BT_PORT = '/dev/ttyS0'  # based on can_BT.py
BAUDRATE = 921600         # use same baudrate as BT_Init() in can_BT.py

def BT_connect(baudrate):
    """Open BT serial port with specified baudrate"""
    return serial.Serial(
        port=BT_PORT,
        baudrate=baudrate,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=0.001
    )

def BT_Tx_Byte(bt_serial, data):
    """Send single line data with termination"""
    bt_serial.write(str.encode(data))
    bt_serial.write(b'\r')
    bt_serial.write(b'\n')

def main():
    try:
        bt_serial = BT_connect(BAUDRATE)

        if not bt_serial.is_open:
            print("Failed to open BT port")
            return

        print("BT port opened. Sending time every 1 second...")

        while True:
            current_time = time.time()
            time_str = f"{current_time:.3f}"  # e.g., "1721806827.123"
            print(f"Sending: {time_str}")
            BT_Tx_Byte(bt_serial, time_str)
            time.sleep(1)

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    except KeyboardInterrupt:
        print("Terminated by user")

    finally:
        if 'bt_serial' in locals() and bt_serial.is_open:
            bt_serial.close()
            print("BT port closed")

if __name__ == "__main__":
    main()
