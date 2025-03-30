import serial
import time
import os
import csv

global GPS_Buf
global GPS_Raw_data
global GPS_DATA

GPS_Buf = ''
GPS_DATA = ''

GPS_serial = None

def GPS_Init():
    global GPS_serial
    try:
        # GPS 시리얼 포트 초기화
        GPS_serial = serial.Serial('/dev/ttyAMA5', baudrate=9600, parity='N', timeout=1)  # GPIO 핀 연결
        # GPS_serial = serial.Serial('/dev/ttyUSB0', baudrate=9600, parity='N', timeout=1)  # USB 연결

        if GPS_serial.isOpen():
            print("GPS connected")
        else:
            print("[GPS_Error] GPS not connected")
    except Exception as e:
        print(f"[GPS_Error] {e}")

def GPS_Op(writer):
    global GPS_Buf
    global GPS_DATA

    try:
        while GPS_serial.in_waiting:
            # GPS 데이터 읽기
            GPS_Raw_data = GPS_serial.readline().decode('ascii', errors='ignore').strip()
            print(f"Raw GPS Data: {GPS_Raw_data}")  # 디버깅용 출력

            # $GPGGA 데이터 처리
            if GPS_Raw_data.startswith("$GPGGA"):
                print(f"Parsed GPS Data: {GPS_Raw_data.split(',')}")
                writer.writerow(["GPS_DATA", *GPS_Raw_data.split(',')])
                return
    except Exception as e:
        print(f"[GPS_Error] {e}")

if __name__ == "__main__":
    GPS_Init()
    print("GPS Init")
    path = "./" + f"Cansat_Log"
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + f'/gps_log.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        while True:
            GPS_Op(writer)