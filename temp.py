import serial
import time

def calculate_checksum(command):
    checksum = 0
    for char in command:
        checksum ^= ord(char)
    return f"{checksum:02X}"

# 시리얼 포트 설정
ser = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(2)  # 포트 안정화를 위해 대기

# 명령어 작성 및 체크섬 계산
command = "VNWRG,01,07"  # 출력 포맷 설정 명령
checksum = calculate_checksum(command)
full_command = f"${command}*{checksum}\r\n"

# 명령어 전송
ser.write(full_command.encode())

# 응답 읽기
response = ser.readline().decode().strip()
print(f"Response: {response}")

# 시리얼 포트 닫기
ser.close()