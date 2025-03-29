import cs_Common.cs_Time
import cs_Common.cs_Camera
import cs_Common.cs_IMU 
import cs_Common.cs_BT
import cs_Common.cs_SD
import cs_Common.cs_GPS 
import os
import csv
import time
import multiprocessing as mp

writer = None
path = None
loop_cnt = 0

def Life_Sign_Op():
    nowtime = cs_Common.cs_Time.Time_Return()
    writer.writerow([nowtime])

    cs_Common.cs_BT.Thread_Tx_Queue.put(b'%'+nowtime.encode())
 
def cs_setup() :
    global writer,path
    print("CANSAT Setup")

    cur_time = cs_Common.cs_Time.Time_Return_second()
    path = "./"+f"Cansat_Log_{cur_time}"
    os.mkdir(path)

    print("Log Path OK")

    f = open(path+f'/cansat_log_{cur_time}.csv', 'w', newline='')
    writer = csv.writer(f)
    cs_Common.cs_Camera.Camera_SetUp(path)
    cs_Common.cs_GPS.GPS_Init()
    cs_Common.cs_IMU.IMU_Init()
    cs_Common.cs_BT.BT_Init()
    
    print("CANSAT Init")


def cs_loop():
    FrameRate = 30  # Setting Operation Cycle

    global writer, path
    startTime = time.time_ns()
    cur_time = cs_Common.cs_Time.Time_Return()
    global loop_cnt 
    
    if loop_cnt % FrameRate == 1:
        Encode_Flag = True
    else:
        Encode_Flag = False

    Life_Sign_Op()
    print(f"loop cnt : {loop_cnt}, Encode : {Encode_Flag}")
    print(f"After Life Sign Op {cs_Common.cs_Time.Time_Return()}")
    cs_Common.cs_Camera.Camera_Op(writer, path,cur_time, Encode_Flag)
    print(f"After Camera Op {cs_Common.cs_Time.Time_Return()}")
    cs_Common.cs_GPS.GPS_Op(writer)
    print(f"After GPS Op {cs_Common.cs_Time.Time_Return()}")
    cs_Common.cs_IMU.IMU_Op(writer)
    print(f"After IMU Op {cs_Common.cs_Time.Time_Return()}")
    if cs_Common.cs_BT.BT_serial.in_waiting:
        USER_CMD = cs_Common.cs_BT.BT_Rx_Op()
        if USER_CMD == "ERROR":
            print("BT Not Connected")
        else:
            print(USER_CMD)
    
    print(f"After BT Rx Op {cs_Common.cs_Time.Time_Return()}")
    
    while time.time_ns() - startTime < 1000000000/FrameRate:
        True

    loop_cnt += 1

if __name__ == "__main__":
    print("OPERATION START")
    cs_setup()

    process_Tx = mp.Process(target=cs_Common.cs_BT.BT_Tx_Thread_Worker,args=(cs_Common.cs_BT.Thread_Tx_Queue,))
    process_Ec = mp.Process(target=cs_Common.cs_Camera.Encoding_Thread_Worker,args=(cs_Common.cs_Camera.Thread_Encoding_Queue,))
    process_Tx.start()
    process_Ec.start()

    while cs_Common.cs_BT.BT_Rx_Op()[0:7] != "CONNECT":  # This checks connection with GS
        True

    while True:
        cs_loop()
            