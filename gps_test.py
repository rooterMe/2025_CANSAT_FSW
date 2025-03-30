import serial

def gps_init():
    try:
        gps_serial = serial.Serial('/dev/ttyAMA1', baudrate=9600, parity='N', timeout=1)
        if gps_serial.isOpen():
            print("GPS connected")
            return gps_serial
        else:
            print("Failed to open GPS serial port")
            return None
    except Exception as e:
        print(f"Error initializing GPS: {e}")
        return None

def read_gps_data(gps_serial):
    buffer = ''
    while True:
        if gps_serial.in_waiting:
            raw_byte = gps_serial.read()
            char = raw_byte.decode('ascii', errors='ignore')
            if char == '\n':
                if buffer.startswith('$GPGGA'):
                    #print("Received GPS GGA Data:")
                    print(buffer.strip())
                buffer = ''
            else:
                buffer += char

if __name__ == "__main__":
    gps = gps_init()
    if gps:
        try:
            read_gps_data(gps)
        except KeyboardInterrupt:
            print("\nTerminated by user")
        finally:
            gps.close()


# temp text