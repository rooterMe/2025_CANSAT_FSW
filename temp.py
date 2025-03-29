import serial
import time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(2)

# 출력 포맷을 $VNQMR로 설정 (예시)
ser.write(b'$VNWRG,01,07*XX\r\n')  # 체크섬 부분은 정확히 계산해서 보내야 함
