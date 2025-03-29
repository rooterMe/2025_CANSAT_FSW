import os
import time
import datetime
from picamera2 import Picamera2
from PIL import Image

def main():
    # 현재 시간 기준 폴더명 생성
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"images_{timestamp}"
    os.mkdir(folder_name)

    # Picamera2 초기화 및 프리뷰 설정
    picam = Picamera2()
    config = picam.create_preview_configuration()
    picam.configure(config)
    picam.start()

    print("카메라 시작됨. 15초 동안 유지하며 3초 간격으로 이미지 캡처")

    for i in range(5):
        image_path = os.path.join(folder_name, f"image_{i+1}.jpg")
        picam.capture_file(image_path)
        print(f"저장됨: {image_path}")
        if i < 4:
            time.sleep(3)

    picam.stop()
    print("카메라 종료")

if __name__ == "__main__":
    main()
