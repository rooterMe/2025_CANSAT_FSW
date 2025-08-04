import gpiod
import time

# GPIO 칩 및 라인 설정
CHIP_NAME     = 'gpiochip0'
SERVO_OFFSET  = 21      # BCM 21 → 물리 핀 40
PWM_FREQUENCY = 50      # 50Hz
PERIOD_SEC    = 1.0 / PWM_FREQUENCY  # 20ms

# gpiod 라인 요청
chip = gpiod.Chip(CHIP_NAME)
servo_line = chip.get_line(SERVO_OFFSET)
servo_line.request(consumer="Servo", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

def servo_move(angle: float, duration: float):
    """
    서보모터를 지정한 각도로 이동시킵니다.
    :param angle: 0~180 (도)
    :param duration: 이동 유지 시간 (초)
    """
    # 각도를 펄스 폭으로 변환 (1ms @0°, 2ms @180°)
    pulse_width = 0.001 + (angle / 180.0) * 0.001  # 1ms + angle*(1ms/180)
    off_time = PERIOD_SEC - pulse_width

    end_time = time.time() + duration
    while time.time() < end_time:
        servo_line.set_value(1)
        time.sleep(pulse_width)
        servo_line.set_value(0)
        time.sleep(off_time)

if __name__ == "__main__":
    try:
        print("서보모터 테스트 시작합니다.")
        # 0°, 90°, 180° 위치로 각각 2초간 이동
        print("→ 0°")
        servo_move(0, 2.0)
        print("→ 90°")
        servo_move(90, 2.0)
        print("→ 180°")
        servo_move(180, 2.0)
        print("→ 90°")
        servo_move(90, 2.0)

    except KeyboardInterrupt:
        print("테스트 중단합니다.")
    finally:
        servo_line.set_value(0)
        servo_line.release()
        chip.close()
        print("GPIO 정리 완료하였습니다.")
