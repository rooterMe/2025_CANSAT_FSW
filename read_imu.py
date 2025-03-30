import serial
import time

# EBIMU-9DOFV4 연결 포트 설정
ser = serial.Serial(
    port='/dev/ttyAMA2',      # 라즈베리파이의 UART 포트
    baudrate=115200,          # 기본 Baudrate
    timeout=1                 # 1초 타임아웃
)

time.sleep(2)  # 시리얼 초기화 대기

print("EBIMU-9DOFV4 데이터 수신 시작...")

try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore')
            print(line.strip())  # 슬라이싱 없이 그대로 출력
except KeyboardInterrupt:
    print("종료됨.")
    ser.close()
