import can_Common.can_Time
import can_Common.can_Camera
import can_Common.can_IMU 
import can_Common.can_BT
#import can_Common.can_SD
import can_Common.can_GPS 
import can_Common.can_Light
import can_Common.can_Servo
import can_Common.can_Targeting
import can_Common.can_Motor
import can_Common.can_Servo
import os
import csv
import time
import math
import multiprocessing as mp
import RPi.GPIO as GPIO
import gpiod

writer = None
path = None
loop_cnt = 0

Lat = -1
Lon = -1
Alt = -1
Lat0 = -1
Lon0 = -1
Alt0 = -1
v_x = 0
v_y = 0
v_z = 0

wing = False
pre_time = None
light_cnt = 0

Left = -1
Right = -1

def Life_Sign_Op():
    nowtime = can_Common.can_Time.Time_Return()
    writer.writerow([nowtime])

    can_Common.can_BT.Thread_Tx_Queue.put(b'%'+nowtime.encode())

def can_setup() :
    global writer,path
    print("CANSAT Setup")

    cur_time = can_Common.can_Time.Time_Return_second()
    path = "./"+f"Cansat_Log_{cur_time}"
    os.mkdir(path)

    print("Log Path OK")

    f = open(path+f'/cansat_log_{cur_time}.csv', 'w', newline='')
    writer = csv.writer(f)
    can_Common.can_Camera.Camera_SetUp(path)
    can_Common.can_GPS.GPS_Init()
    can_Common.can_IMU.IMU_Init()
    can_Common.can_BT.BT_Init()
    can_Common.can_Motor.Motor_Init()

def can_loop():
    FrameRate = 30  # Setting Operation Cycle

    global writer, path
    startTime = time.time_ns()
    cur_time = can_Common.can_Time.Time_Return()
    global loop_cnt 
    
    if loop_cnt % FrameRate == 1:
        Encode_Flag = True
    else:
        Encode_Flag = False

    global Lat, Lon, Alt, Lat0, Lon0, Alt0, v_x, v_y, v_z
    global Left, Right

    Life_Sign_Op()
    print(f"loop cnt : {loop_cnt}, Encode : {Encode_Flag}")
    print(f"After Life Sign Op {can_Common.can_Time.Time_Return()}")
    can_Common.can_Camera.Camera_Op(writer, path,cur_time, Encode_Flag)
    print(f"After Camera Op {can_Common.can_Time.Time_Return()}")

    res = can_Common.can_GPS.GPS_Op(writer)
    if res is not None:
        Lat_c, Lon_c, Alt_c = res
    else:
        Lat_c, Lon_c, Alt_c = None, None, None
    #Lat_c, Lon_c, Alt_c = can_Common.can_GPS.GPS_Op(writer)
    print(f"After GPS Op {can_Common.can_Time.Time_Return()}")
    if Lat_c is not None and Lon_c is not None and Alt_c is not None:
        if Lat0 == -1 and Lon0 == -1 and Alt0 == -1:
            Lat0, Lon0, Alt0 = Lat_c, Lon_c, Alt_c
        Lat, Lon, Alt = Lat_c, Lon_c, Alt_c
    IMU_data = can_Common.can_IMU.IMU_Op(writer)
    if IMU_data is not None:
        v_x, v_y, v_z = float(IMU_data[4]), float(IMU_data[5]), float(IMU_data[6])
    print(f"After IMU Op {can_Common.can_Time.Time_Return()}")
    
    print("***************************")
    print(f"Lat : {Lat}, Lon : {Lon}, Alt : {Alt}")
    print(f"v_x : {v_x}, v_y : {v_y}, v_z : {v_z}")
    print("***************************")

    global wing, pre_time

    if wing:
        can_Common.can_Servo.open_wing()
        Left = 0
        Right = 0
        pre_time = time.time()
        wing = False

    if not wing and pre_time is not None and (time.time() - pre_time) > 5:
        if Lat0 != -1 and Lon0 != -1 and Lat0 != Lat and Lon0 != Lon:
            ans = can_Common.can_Targeting.control_to_target(Lat, Lon, Lat0, Lon0, v_x, v_y, v_z)
            if ans == -1:
                can_Common.can_Motor.change_wing(writer, 0-Left, 1-Right)
                Left = 0
                Right = 1
            elif ans == 0:
                can_Common.can_Motor.change_wing(writer, 1-Left, 1-Right)
                Left = 1
                Right = 1
            elif ans == 1:
                can_Common.can_Motor.change_wing(writer, 1-Left, 0-Right)
                Left = 1
                Right = 0


    if can_Common.can_BT.BT_serial.in_waiting:
        USER_CMD = can_Common.can_BT.BT_Rx_Op()
        if USER_CMD == "ERROR":
            print("BT Not Connected")
        elif USER_CMD == "WINGOPEN":
            #global wing
            wing = True
            can_Common.can_BT.Thread_Tx_Queue.put(b'WINGOPENok')
        elif USER_CMD == "TURNLEFT":
            can_Common.can_Motor.change_wing(writer, 0-Left, 1-Right)
            Left = 0
            Right = 1
            can_Common.can_BT.Thread_Tx_Queue.put(b'TURNLEFTok')
        elif USER_CMD == "TURNRIGHT":
            can_Common.can_Motor.change_wing(writer, 1-Left, 0-Right)
            Left = 1
            Right = 0
            can_Common.can_BT.Thread_Tx_Queue.put(b'TURNRIGHTok')
        elif USER_CMD == "MAINTAIN":
            can_Common.can_Motor.change_wing(writer, 1-Left, 1-Right)
            Left = 1
            Right = 1
            can_Common.can_BT.Thread_Tx_Queue.put(b'MAINTAINok')
        else:
            print(USER_CMD)
    print(f"After BT Rx Op {can_Common.can_Time.Time_Return()}")
    
    
    while time.time_ns() - startTime < 1000000000 / FrameRate:
        True
    
    loop_cnt += 1

if __name__ == "__main__":
    print("OPERATION START")
    can_setup()
    print("1")
    process_Tx = mp.Process(target=can_Common.can_BT.BT_Tx_Thread_Worker,args=(can_Common.can_BT.Thread_Tx_Queue,))
    process_Ec = mp.Process(target=can_Common.can_Camera.Encoding_Thread_Worker,args=(can_Common.can_Camera.Thread_Encoding_Queue,))
    print("2")
    process_Tx.start()
    process_Ec.start()
    print("3")
    while can_Common.can_BT.BT_Rx_Op()[0:7] != "CONNECT": # This chekcs connection with GS
        print("Waiting for connection...")
        time.sleep(1)
    print("Connected to GS")

    while True:
        can_loop()
