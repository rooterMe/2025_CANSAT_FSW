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

def change_wing(writer, left, right):
   

    # 왼쪽 날개 제어
    if left == 1:
        MOTOR_csv(writer, "Motor", "Left", "Up")
    elif left == -1:
        MOTOR_csv(writer, "Motor", "Left", "Down")
        
    if right == 1:
        MOTOR_csv(writer, "Motor", "Right", "Up")
    elif right == -1:
        MOTOR_csv(writer, "Motor", "Right", "Down")
