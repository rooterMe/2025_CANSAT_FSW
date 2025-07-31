import RPi.GPIO as GPIO
import time

# BCM 방식 GPIO 번호 정의
IN1 = 17  # 물리 핀 11 → 모터 A IN1
IN2 = 27  # 물리 핀 13 → 모터 A IN2
IN3 = 22  # 물리 핀 15 → 모터 B IN3
IN4 = 23  # 물리 핀 16 → 모터 B IN4

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT, initial=GPIO.LOW)

def test_motor(pin_forward, pin_backward, duration=1.0):
    """
    지정된 두 핀으로 모터를 한 방향 회전시킵니다.
    :param pin_forward: 전진 신호 GPIO
    :param pin_backward: 후진 신호 GPIO
    :param duration: 회전 시간(초)
    """
    GPIO.output(pin_forward, GPIO.HIGH)
    GPIO.output(pin_backward, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(pin_forward, GPIO.LOW)

try:
    # 모터 A 테스트
    print("모터 A 전진 테스트")
    test_motor(IN1, IN2, duration=2.0)
    print("모터 A 후진 테스트")
    test_motor(IN2, IN1, duration=2.0)

    # 모터 B 테스트
    print("모터 B 전진 테스트")
    test_motor(IN3, IN4, duration=2.0)
    print("모터 B 후진 테스트")
    test_motor(IN4, IN3, duration=2.0)

finally:
    # 테스트 종료 후 GPIO 상태 해제
    GPIO.cleanup()
    print("GPIO 클린업 완료")
