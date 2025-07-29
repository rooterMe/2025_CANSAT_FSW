import can_Common.can_Time
import can_Common.can_Camera
import can_Common.can_IMU 
import can_Common.can_BT
#import can_Common.can_SD
import can_Common.can_GPS 
import os
import csv
import time
import multiprocessing as mp

writer = None
path = None
loop_cnt = 0


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

    Life_Sign_Op()
    print(f"loop cnt : {loop_cnt}, Encode : {Encode_Flag}")
    print(f"After Life Sign Op {can_Common.can_Time.Time_Return()}")
    can_Common.can_Camera.Camera_Op(writer, path,cur_time, Encode_Flag)
    print(f"After Camera Op {can_Common.can_Time.Time_Return()}")
    can_Common.can_GPS.GPS_Op(writer)
    print(f"After GPS Op {can_Common.can_Time.Time_Return()}")
    can_Common.can_IMU.IMU_Op(writer)
    print(f"After IMU Op {can_Common.can_Time.Time_Return()}")
    
    if can_Common.can_BT.BT_serial.in_waiting:
        USER_CMD = can_Common.cs_BT.BT_Rx_Op()
        if USER_CMD == "ERROR":
            print("BT Not Connected")
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
