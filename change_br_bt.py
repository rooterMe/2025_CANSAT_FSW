import serial
import time

def BT_send_command(ser, command):
    """Send AT command and wait for response"""
    print(f"Sending: {command.strip()}")
    ser.write(command.encode())
    time.sleep(0.1)

    response = b""
    while ser.in_waiting:
        response += ser.read()
    print("Response:", response.decode(errors='ignore').strip())
    return response

def main():
    # Step 1: connect to current baudrate (921600)
    ser = serial.Serial('/dev/ttyS0', baudrate=921600, timeout=0.1)
    if not ser.is_open:
        print("Failed to open serial port")
        return

    print("Connected to BT module at 921600")

    # Step 2: send AT command to set baudrate to 115200
    BT_send_command(ser, 'AT+UARTCONFIG,115200,N,1,0\r\n')
    time.sleep(0.2)

    ser.close()
    print("Port closed after baudrate change")

    # Step 3: wait and reconnect at new baudrate
    time.sleep(0.5)
    ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=0.1)
    if ser.is_open:
        print("Reconnected at 115200")
        BT_send_command(ser, 'AT\r')
    else:
        print("Failed to reconnect at 115200")

    ser.close()

if __name__ == "__main__":
    main()
