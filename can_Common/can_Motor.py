import gpiod
import time
import can_Common.can_BT
import csv

# GPIO 칩 및 모터 제어 라인 offset 정의
CHIP_NAME    = 'gpiochip0'
IN1_OFFSET   = 17  # Left Up
IN2_OFFSET   = 27  # Left Down
IN3_OFFSET   = 22  # Right Up
IN4_OFFSET   = 23  # Right Down

# GPIO 칩 열기 및 라인 요청
chip = gpiod.Chip(CHIP_NAME)
in1 = chip.get_line(IN1_OFFSET)
in2 = chip.get_line(IN2_OFFSET)
in3 = chip.get_line(IN3_OFFSET)
in4 = chip.get_line(IN4_OFFSET)
for line, name in [(in1, "IN1"), (in2, "IN2"), (in3, "IN3"), (in4, "IN4")]:
    line.request(consumer=name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

def MOTOR_csv(writer, motor, side, direction):
    """
    CSV에 기록하고 블루투스로 전송합니다.
    :param writer: csv.writer 객체
    :param motor: "Motor" 등 식별 문자열
    :param side: "Left" 또는 "Right"
    :param direction: "Up" 또는 "Down"
    """
    # 1) CSV 기록
    writer.writerow([motor, side, direction])
    # 2) 블루투스 전송 포맷 생성 및 전송
    data = f"!,{motor},{side},{direction}"
    can_Common.can_BT.Thread_Tx_Queue.put(data.encode())

def left_up(duration, writer):
    in1.set_value(1); in2.set_value(0)
    in3.set_value(0); in4.set_value(0)
    MOTOR_csv(writer, "Motor", "Left", "Up")
    time.sleep(duration)
    in1.set_value(0)

def left_down(duration, writer):
    in1.set_value(0); in2.set_value(1)
    in3.set_value(0); in4.set_value(0)
    MOTOR_csv(writer, "Motor", "Left", "Down")
    time.sleep(duration)
    in2.set_value(0)

def right_up(duration, writer):
    in1.set_value(0); in2.set_value(0)
    in3.set_value(1); in4.set_value(0)
    MOTOR_csv(writer, "Motor", "Right", "Up")
    time.sleep(duration)
    in3.set_value(0)

def right_down(duration, writer):
    in1.set_value(0); in2.set_value(0)
    in3.set_value(0); in4.set_value(1)
    MOTOR_csv(writer, "Motor", "Right", "Down")
    time.sleep(duration)
    in4.set_value(0)

def left_down_right_up(duration, writer):
    in1.set_value(0); in2.set_value(1)  # Left Down
    in3.set_value(1); in4.set_value(0)  # Right Up
    MOTOR_csv(writer, "Motor", "Left", "Down")
    MOTOR_csv(writer, "Motor", "Right", "Up")
    time.sleep(duration)
    in2.set_value(0); in3.set_value(0)

def right_down_left_up(duration, writer):
    in1.set_value(1); in2.set_value(0)  # Left Up
    in3.set_value(0); in4.set_value(1)  # Right Down
    MOTOR_csv(writer, "Motor", "Left", "Up")
    MOTOR_csv(writer, "Motor", "Right", "Down")
    time.sleep(duration)
    in1.set_value(0); in4.set_value(0)

# 사용 예시
if __name__ == "__main__":
    with open("motor_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # 예: 왼쪽 상승 1초, 오른쪽 하강 1초, 동시 동작 2초
        left_up(1.0, writer)
        right_down(1.0, writer)
        left_down_right_up(2.0, writer)

    # GPIO 라인 해제
    for line in (in1, in2, in3, in4):
        line.release()
