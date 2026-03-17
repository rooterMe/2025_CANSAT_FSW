# 2025_CANSAT_FSW

> FLight Software Program for 2025 CANSAT Competition Korea
> 
> These files are used on the Raspberry Pi.
> 
> If you want to see about AI of this project, visit [this link](https://github.com/rooterMe/2025_CANSAT_AI)
>
> If you want to see about Ground Station Program of this project, visit [this link](https://github.com/rooterMe/2025_CANSAT_GS)
>
> by [Kangmin Ra](https://github.com/rooterMe)(35th), [Cheolsoon Han](https://github.com/cheolsoon1234)(34th)

2025년 캔위성 대회에서 사용했던 FSW입니다. 2025년에는 대회측에서 제공해주는 캔위성 키트를 사용하지 않고, 라즈베리파이 기반에 캔위성을 직접 설계 및 제작해 사용했습니다. 라즈베리파이 내 VS Code에서 실행하여 사용할 수 있습니다. 캔위성 및 프로그램 코드 관련해서 문의가 있으면 rooterme@kaist.ac.kr로 문의 바랍니다.

# Code Overview

## `can_main_v0.py`

라즈베리파이 내의 VSC에서 can_main 파일을 실행하여 작동시킵니다. can_Common 폴더의 다른 파일들을 호출하며 실행합니다.

이 repository에 v0~3까지 있는데 v0를 보시면 됩니다. 다른 버전은 2025년 대회를 위한 코드가 추가되어있습니다.

```python
    while can_Common.can_BT.BT_Rx_Op()[0:7] != "CONNECT": # This chekcs connection with GS
        print("Waiting for connection...")
        time.sleep(1)
    print("Connected to GS")

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

### `can_Camera`


<!--

-->
