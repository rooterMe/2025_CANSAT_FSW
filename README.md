# 2025_CANSAT_FSW

> Flight Software Program for 2025 CANSAT Competition Korea
> 
> These files are used on the Raspberry Pi.
> 
> If you want to see about AI of this project, visit [this link](https://github.com/rooterMe/2025_CANSAT_AI)
>
> If you want to see about Ground Station Program of this project, visit [this link](https://github.com/rooterMe/2025_CANSAT_GS)
>
> by [Kangmin Ra](https://github.com/rooterMe)(35th), [Cheolsoon Han](https://github.com/cheolsoon1234)(34th)

2025년 캔위성 경연대회에서 사용했던 FSW입니다. 2025년에는 대회측에서 제공해주는 캔위성 키트를 사용하지 않고, 라즈베리파이 기반에 캔위성을 직접 설계 및 제작해 사용했습니다. 라즈베리파이 내 VS Code에서 실행하여 사용할 수 있습니다. 캔위성 및 프로그램 코드 관련해서 문의사항 있으면 rooterme@kaist.ac.kr로 연락해주시길 바랍니다.

# Code Overview

> GPS, IMU 등의 모든 센서값은 라즈베리파이 내부에 저장하도록 되어있습니다. 내부 디렉토리에 csv 파일이 생성되어 값을 저장합니다.

## `can_main_v0.py`

라즈베리파이 내의 VSC에서 can_main 파일을 실행하여 작동시킵니다. can_Common 폴더의 다른 파일들을 호출하며 실행합니다.

이 repository에 v0~3까지 있는데 v0를 보시면 됩니다. 다른 버전은 2025년 대회를 위한 코드가 추가되어있습니다.

```python
    while can_Common.can_BT.BT_Rx_Op()[0:7] != "CONNECT": # This chekcs connection with GS

    while True:
        can_loop()
```

캔위성의 BT센서와 연결되면 CONNECT 신호를 받습니다. `can_main` 코드 실행 후 BT 연결이 확인되면 **can_loop**가 돌아갑니다.

**can_loop** 에서는 카메라, GPS, IMU, BT 등의 센서를 호출하고 작동을 확인합니다.

## `can_Common`

`can_Common` 폴더에는 GPS, IMU 등 세부적인 센서에 대한 코드들이 포함되어있습니다. `can_main`에서 이 파일 내의 코드들을 사용합니다.

이 폴더의 파일 중 `can_BT.py`, `can_Camera.py`, `can_GPS.py`, `can_IMU.py`, `can_Time.py` 만 보시면 됩니다. 다른 파일들은 2025년 임무를 위한 추가적인 코드입니다. 

### `can_BT.py`

**BT_Rx_Op** 가 실행되는 함수 부분입니다. BT 센서가 읽은 데이터들을 **BT_Buf**에 저장해 Q로 반환합니다.

파일 내 다양한 함수가 있습니다. Baudrate 설정 등 명령어를 보낼 수 있도록 간편화 해두었습니다. 함수의 역할은 각 함수별로 주석이 적혀있습니다. 추가적인 명령어 관련은 Cansat 대회측에서 제공하는 자료나 BT 센서 메뉴얼을 직접 찾아보시면 됩니다. 

이 파일은 직접 실행하지 않고 main에서 호출되어 사용합니다. 디버깅을 위해 직접 실행하실 수 있습니다.

### `can_Camera.py`

Operation이 호출될 때마다 사진을 촬영합니다. picamera module 사용합니다.

촬영된 사진은 BT로 지상국으로 전송되며 라즈베리파이 내부에 직접 저장됩니다. 지상국으로 전송되는 주기는 `can_main.py` 및 `can_Camera.py`를 통해 변경할 수 있습니다.

BT 전송은 라즈베리파이 내에서 base64로 encoding 하여 전송됩니다. 지상국에서는 decode하는 코드로 수신된 사진을 확인할 수 있습니다.

사진의 size는 필요에 따라 화질을 변경해도 좋지만 BT 센서의 시간당 전송가능용량을 고려하셔야 합니다.

### `can_GPS.py`

```python
# $GPGGA,,,,,,0,00,,,M,0.0,M,,0000*48\r\n
        if GPS_Buf == "$":
            if GPS_DATA[0:6] == "$GPGGA":  # 원하는 데이터 형식 수신시 처리
                a = GPS_DATA.split(',')
                Lat, Lon, Alt = a[2], a[4], a[9]
                writer.writerow(["GPS_DATA", *map(lambda x: str(x), GPS_DATA.split(','))])
```
위도, 경도, 고도 등 필요한 데이터는 $GPGGA로 시작하여 데이터가 들어옵니다. 다른 정보가 필요할 경우 직접 센서 메뉴얼을 확인하시고 코드 수정하시면 됩니다.

학교에 GPS 센서 여유분이 어느정도 있습니다. 다만 일부 센서는 고장난 센서입니다.

충북과학고 부지 내에서는 GPS 신호가 거의 잡히지 않았었습니다. 웬만하면 캔위성 대회측에서 제공받은 새 GPS 센서를 사용하는게 좋습니다.

### `can_IMU.py`

IMU 센서는 Roll, Pitch, Yaw 각 축별 pos나 x,y,z 축별 선형 가속도를 측정하는 센서입니다. 다른 센서들과 마찬가지로 간편화된 함수가 있고, BT로 전송합니다.

IMU 센서 메뉴얼 찾아보면 위 정보 말고 다른 데이터도 수신할 수 있도록 mode 변경할 수 있으니 직접 mode 변경하고 코드 수정하면 됩니다.

### `can_Time.py`

호출시 현재 시간을 반환하도록 되어있는 함수입니다. 로그 내부저장시 시간 기록을 위해 사용됩니다.

---

추가적으로 설명하자면
```python
GPS_serial = serial.Serial('/dev/ttyAMA2', baudrate=9600, parity='N', timeout=0.001)  # when connect to GPIO pins (RX: GPIO 4 TX: GPIO 5)
GPS_serial = serial.Serial('COM5', baudrate=9600, parity='N', timeout=0.001)  # when connect to USB
```
이와 같이 Serial 연결코드가 있을 때
- 라즈베리파이 내에서 사용할 때에는  ttyAMAn 같이 라즈베리파이 회로에 맞게 설명하면 되고
- 디버깅, 연결확인 등을 위해 노트북에 직접 연결할 때에는 장치관리자에서 Port 확인하고 아래 코드처럼 하면 됩니다.

---
이 외에 나머지 파일들은 Test 파일들입니다. 라즈베리파이에서 BT, GPS, IMU 등의 센서들 작동 확인을 위한 단순 코드입니다. 

<!--

-->
