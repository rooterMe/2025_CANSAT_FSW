import can_Common.can_BT
import RPi.GPIO as GPIO
import time




def setServoPos(servo, degree):
  # 각도는 180도를 넘을 수 없다.
  if degree > 180:
    degree = 180

  # 각도(degree)를 duty로 변경한다.
  duty = 3+(degree*(12-3)/180.0)
  # duty 값 출력
  print("Degree: {} to {}(Duty)".format(degree, duty))

  # 변경된 duty값을 서보 pwm에 적용
  servo.ChangeDutyCycle(duty)

if __name__ == "__main__":
    servoPin          = 32   # 서보 핀

    GPIO.setmode(GPIO.BOARD)        # GPIO 설정
    GPIO.setup(servoPin, GPIO.OUT)  # 서보핀 출력으로 설정

    servo = GPIO.PWM(servoPin, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
    servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.

    setServoPos(servo, 0)
    time.sleep(1) 

    # 서보 PWM 정지
    servo.stop()
    # GPIO 모드 초기화
    GPIO.cleanup()