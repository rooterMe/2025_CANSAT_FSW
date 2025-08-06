# can_Common/can_Motor.py

import gpiod
import can_Common.can_BT
import time
import csv


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

def Motor_Init():
    """
    모터 초기화 함수입니다.
    GPIO 핀을 설정하고, 모터를 초기화합니다.
    """
    print("Motor Init")
    # GPIO 핀 설정
    CHIP_NAME = 'gpiochip0'
    IN1_OFFSET = 17  # Left Up
    IN2_OFFSET = 27  # Left Down
    IN3_OFFSET = 22  # Right Up
    IN4_OFFSET = 23  # Right Down

    # GPIO 칩 열기 및 라인 요청
    chip = gpiod.Chip(CHIP_NAME)
    in1 = chip.get_line(IN1_OFFSET)
    in2 = chip.get_line(IN2_OFFSET)
    in3 = chip.get_line(IN3_OFFSET)
    in4 = chip.get_line(IN4_OFFSET)

    for line, name in [(in1, "IN1"), (in2, "IN2"), (in3, "IN3"), (in4, "IN4")]:
        line.request(consumer=name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    
    for line in (in1, in2, in3, in4):
        line.set_value(0)

def change_wing(writer, left, right):
    """
    좌우 날개 상태(left, right)에 따라 GPIO를 제어하고
    MOTOR_csv를 호출합니다.
    :param writer: csv.writer 객체
    :param left: 왼쪽 날개 명령 (1=Up, -1=Down, 0=Maintain)
    :param right: 오른쪽 날개 명령 (1=Up, -1=Down, 0=Maintain)
    """
    # GPIO 핀 설정
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

    # 왼쪽 날개 제어
    if left == 1:
        in1.set_value(1); in2.set_value(0)
        MOTOR_csv(writer, "Motor", "Left", "Up")
    elif left == -1:
        in1.set_value(0); in2.set_value(1)
        MOTOR_csv(writer, "Motor", "Left", "Down")
    else:
        in1.set_value(0); in2.set_value(0)
    # 오른쪽 날개 제어
    if right == 1:
        in3.set_value(1); in4.set_value(0)
        MOTOR_csv(writer, "Motor", "Right", "Up")
    elif right == -1:
        in3.set_value(0); in4.set_value(1)
        MOTOR_csv(writer, "Motor", "Right", "Down")
    else:
        in3.set_value(0); in4.set_value(0)

    # (필요 시) 짧은 동작 유지 후 해제
    time.sleep(1)
    # GPIO 해제
    for line in (in1, in2, in3, in4):
        line.set_value(0)
