import gpiod
import time

# GPIO 칩 및 모터 제어 라인 offset 정의
CHIP_NAME = 'gpiochip0'
IN1_OFFSET = 17  # 물리 핀 11 → 모터 A IN1
IN2_OFFSET = 27  # 물리 핀 13 → 모터 A IN2
IN3_OFFSET = 22  # 물리 핀 15 → 모터 B IN3
IN4_OFFSET = 23  # 물리 핀 16 → 모터 B IN4

# GPIO 칩 열기
chip = gpiod.Chip(CHIP_NAME)

# 각 라인 객체 가져오기
in1 = chip.get_line(IN1_OFFSET)
in2 = chip.get_line(IN2_OFFSET)
in3 = chip.get_line(IN3_OFFSET)
in4 = chip.get_line(IN4_OFFSET)

# 출력 모드로 요청 (기본값 0)
in1.request(consumer="MotorIN1", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
in2.request(consumer="MotorIN2", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
in3.request(consumer="MotorIN3", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
in4.request(consumer="MotorIN4", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

def test_motor(pin_forward, pin_backward, duration=1.0):
    """
    지정된 두 라인을 이용해 모터를 한 방향 회전시킵니다.
    :param pin_forward: 전진 신호 라인 객체
    :param pin_backward: 후진 신호 라인 객체
    :param duration: 회전 시간(초)
    """
    # 전진
    pin_forward.set_value(1)
    pin_backward.set_value(0)
    time.sleep(duration)
    # 정지
    pin_forward.set_value(0)

try:
    # 모터 A 테스트
    print("모터 A 전진 테스트입니다.")
    test_motor(in1, in2, duration=2.0)
    print("모터 A 후진 테스트입니다.")
    test_motor(in2, in1, duration=2.0)

    # 모터 B 테스트
    print("모터 B 전진 테스트입니다.")
    test_motor(in3, in4, duration=2.0)
    print("모터 B 후진 테스트입니다.")
    test_motor(in4, in3, duration=2.0)

finally:
    # 모든 라인 해제
    in1.release()
    in2.release()
    in3.release()
    in4.release()
    print("GPIO 라인 해제 완료입니다.")
