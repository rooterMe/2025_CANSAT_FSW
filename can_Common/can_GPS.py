import serial
import time
import os
import csv
import can_Common.can_BT

global GPS_serial
global GPS_Buf
global GPS_Raw_data
global GPS_DATA

GPS_Buf = ''
GPS_DATA = ''

GPS_serial = None

def GPS_Init() :
    global GPS_serial
    GPS_serial = serial.Serial('/dev/ttyAMA2', baudrate=9600, parity='N', timeout=0.001)  # when connect to GPIO pins (RX: GPIO 4 TX: GPIO 5)
    #GPS_serial = serial.Serial('COM5', baudrate=9600, parity='N', timeout=0.001)  # when connect to USB

    if GPS_serial.isOpen() == True:
        print("GPS connected")

    else:
        print("[GPS_Error] GPS not connected")


def GPS_Op(writer):
    global GPS_Buf
    global GPS_DATA

    # print(str(GPS_serial.read()))
    #print(GPS_Buf)
    while GPS_serial.in_waiting:
        # print(GPS_serial.in_waiting)

        GPS_Raw_data = str(GPS_serial.read()) 
        #print(GPS_Raw_data)
        GPS_Buf += GPS_Raw_data
        GPS_Buf = GPS_Buf.replace("'", "")
        GPS_Buf = GPS_Buf.replace("b", "")
        GPS_Buf = GPS_Buf.replace("r", "")
        GPS_Buf = GPS_Buf.replace("n", "")
        GPS_Buf = GPS_Buf.replace("\\", "")
        
        # $GPGGA,,,,,,0,00,,,M,0.0,M,,0000*48\r\n
        if GPS_Buf == "$":
            # print(GPS_DATA[:-4])

            if GPS_DATA[0:6] == "$GPGGA":  # 원하는 데이터 형식 수신시 처리

                print(GPS_DATA.split(','))
                a = GPS_DATA.split(',')
                Lat, Lon, Alt = float(a[1]), float(a[3]), float(a[9])
                writer.writerow(["GPS_DATA", *map(lambda x: str(x), GPS_DATA.split(','))])

                # BT Operation
                #Lat, Lon, Alt = a[1], a[3], a[9]
                can_Common.can_BT.Thread_Tx_Queue.put(GPS_DATA.encode())

                GPS_DATA = ""
                return Lat, Lon, Alt  # return GPS DATA
            
            GPS_DATA = ""
            return None, None, None # no GPS DATA

        GPS_DATA += GPS_Buf
        GPS_Buf = ""


if __name__ == "__main__":
    GPS_Init()
    print("GPS Init")
    path = "./"+f"Cansat_Log"
    # os.mkdir(path)
    f = open(path+f'/gps_log{time.time()}.csv', 'w', newline='')
    writer = csv.writer(f)
    while( True ):
        GPS_Op(writer)








