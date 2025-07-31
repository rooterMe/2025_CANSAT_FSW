# 2025_CANSAT_FSW

2025년 캔위성 경연대회 FSW

## 원하는 목표로 낙하하는 캔위성 개발 (주제명 미정, 팀 이름 미정)

### 캔위성 하드웨어

캔위성을 기존 방식처럼 낙하산을 통해 낙하하는 것이 아닌 로켓에서 캔위성이 사출되면 글라이더 형식의 날개를 전개하여 활강하며 낙하하는 비행체의 방식
낙하 과정에서 상승타, 방향 제어 필요

라즈베리 활용 직접 제작

#### 상승타 - 활강제어

상승타 제어를 통한 활강 제어

IMU 센서 값에 따른 상승타 각도 제어

- 캔위성 각도 양 -> 상승타 각도 음 -> 앞으로 회전
- 캔위성 각도 양 -> 상승타 각도 양 -> 활강

#### ??? - 좌우제어

- 좌우제어 방안 모색중 

#### test 해야할 것

- 진동시험, 충격시험

### 캔위성 소프트웨어

라즈베리파이 사용

IMU, GPS 등 센서값 데이터 수집 (CSV 파일 제작 코드 필요)

[임시] IMU 값에 따른 상승타 모터 제어 코드 필요

IMU 값 Roll, Pitch, Yaw만 출력됨 (가속도, 자이로 출력 안됨, 수정 필요)

(New!)전압센서 -> 베터리 전압, 전류

(New!)기압계 -> 고도 교차검증

### 인공지능

### 지상국

(New!)코드 응답속도 비교

(New!)스레딩 -> 멀티프로세싱 (코어 분리)

(New!)통신모듈 2개? 관측자료/ 텔레메트리, 비콘신호 분리

CBSH@raspberrypi:~/Desktop/cansat 2025 v2 $ pip3 install rpi-lgpio
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
CBSH@raspberrypi:~/Desktop/cansat 2025 v2 $ pip install rpi-lgpio
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
CBSH@raspberrypi:~/Desktop/cansat 2025 v2 $ pip uninstall RPi.GPIO
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
CBSH@raspberrypi:~/Desktop/cansat 2025 v2 $ pip install rpi-lgpio
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    For more information visit http://rptl.io/venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
