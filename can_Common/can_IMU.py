import serial
import csv
from queue import Queue
#import can_Common.can_BT

IMU_Rx_Queue = Queue()

global IMU_Buf
global IMU_Raw_Data
global IMU_Data
global Received_IMU_Data
global IMU_Rx_Data
global IMU_Rx_Data_Byte
global IMU_Data_Size

global IMU_serial

# IMU_serial = serial.Serial('COM3', 115200, stopbits=1, parity='N', timeout=0.001)

# ---------------------------------------------------- IMU Command ----------------------------------------------------


def IMU_reset():
    print("IMU Reset")
    IMU_serial.write(b'<reset>')
    IMU_Rx_Op()


def IMU_Cfg():
    print("IMU Configuration")
    IMU_serial.write(b'<cfg>')

    # IMU_Rx_Op()  # For OK Responce
    Get_Cfg_Data()  # For Configuration Data


def IMU_Output_Rate_polling():
    print("IMU Mode Polling")
    IMU_serial.write(b'<sor0>\r')
    IMU_Rx_Op()  # For OK Responce


def IMU_Output_Rate_1():
    IMU_serial.write(b'<sor1>\r')
    IMU_Rx_Op()  # For OK Responce


def IMU_Output_Rate_10():
    IMU_serial.write(b'<sor10>\r')
    IMU_Rx_Op()  # For OK Responce


def IMU_Output_Rate_100():
    IMU_serial.write(b'<sor100>\r')
    IMU_Rx_Op()  # For OK Responce


def IMU_Output_Rate_1000():
    IMU_serial.write(b'<sor1000>\r')
    IMU_Rx_Op()  # For OK Responce


def IMU_Output_Rate_400():
    IMU_serial.write(b'<sor400>\r')
    IMU_Rx_Op()  # For OK Responce


def IMU_115200():
    IMU_serial.write(b'<sb5>\r')
    IMU_Rx_Op()  # For OK Responce


def IMU_921600():
    IMU_serial.write(b'<sb8>\r')
    IMU_Rx_Op()


def IMU_Output_Euler():
    IMU_serial.write(b'<sof0>\r')
    IMU_Rx_Op()


def IMU_Output_Quaternion():
    IMU_serial.write(b'<sof1>\r')
    IMU_Rx_Op()


def IMU_Output_Code_ASCII():
    IMU_serial.write(b'<soc1>\r')
    IMU_Rx_Op()


def IMU_Output_Code_HEX():
    IMU_serial.write(b'<soc2>\r')
    IMU_Rx_Op()

# --------------------- Sensor Setting ---------------------------


def IMU_Set_Acc_OFF():
    IMU_serial.write(b'<soa0>\r')
    IMU_Rx_Op()


def IMU_Set_Acc_ON():
    IMU_serial.write(b'<soa1>\r')
    IMU_Rx_Op()


def IMU_Set_Velo_Local():
    IMU_serial.write(b'<soa4>\r')
    IMU_Rx_Op()


def IMU_Set_Velo_Global():
    IMU_serial.write(b'<soa5>\r')
    IMU_Rx_Op()


def IMU_Set_Gyro_OFF():
    IMU_serial.write(b'<sog0>\r')
    IMU_Rx_Op()


def IMU_Set_Gyro_ON():
    IMU_serial.write(b'<sog1>\r')
    IMU_Rx_Op()


def IMU_Set_Temp_OFF():
    IMU_serial.write(b'<sot0>\r')
    IMU_Rx_Op()


def IMU_Set_Temp_ON():
    IMU_serial.write(b'<sot1>\r')
    IMU_Rx_Op()


def IMU_Set_Distance_OFF():
    IMU_serial.write(b'<sod0>\r')
    IMU_Rx_Op()


def IMU_Set_Distance_Local():
    IMU_serial.write(b'<sod1>\r')
    IMU_Rx_Op()


def IMU_Set_Distance_Global():
    IMU_serial.write(b'<sod2>\r')
    IMU_Rx_Op()


def IMU_Set_Magneto_OFF():
    IMU_serial.write(b'<sem0>\r')
    IMU_Rx_Op()


def IMU_Set_Magneto_ON():
    IMU_serial.write(b'<sem1>\r')
    IMU_Rx_Op()


# ------------------- Accelerometer Setting -------------------
def IMU_Set_Sens_Acc_2G():
    IMU_serial.write(b'<ssa1>\r')
    IMU_Rx_Op()


def IMU_Set_Sens_Acc_4G():
    IMU_serial.write(b'<ssa2>\r')
    IMU_Rx_Op()


def IMU_Set_Sens_Acc_8G():
    IMU_serial.write(b'<ssa3>\r')
    IMU_Rx_Op()


def IMU_Set_Sens_Acc_16G():
    IMU_serial.write(b'<ssa4>\r')
    IMU_Rx_Op()

# ------------------- Gyroscope Setting -------------------


def IMU_Set_Sens_Gyro_250dps():
    IMU_serial.write(b'<ssg1>\r')
    IMU_Rx_Op()


def IMU_Set_Sens_Gyro_500dps():
    IMU_serial.write(b'<ssg2>\r')
    IMU_Rx_Op()


def IMU_Set_Sens_Gyro_1000dps():
    IMU_serial.write(b'<ssg3>\r')
    IMU_Rx_Op()


def IMU_Set_Sens_Gyro_2000dps():
    IMU_serial.write(b'ssg4>\r')
    IMU_Rx_Op()

# ------------------------- Operation -------------------------

# def IMU_Op(writer=None,Flag=False):
#     IMU_DATA = ""    
#     while len(IMU_DATA.split(','))<15:
#         IMU_serial.write(b'*')

#         IMU_DATA += str(IMU_serial.read(IMU_serial.in_waiting))
#         if len(IMU_DATA)>=3: print(IMU_DATA)
#         IMU_DATA = IMU_DATA.replace("*", "")
#         IMU_DATA = IMU_DATA.replace("'", "")
#         IMU_DATA = IMU_DATA.replace("b", "")
#         index = IMU_DATA.find(r"\r\n")
#         IMU_DATA = copy.deepcopy(IMU_DATA[:index])
#         #print(f'IMU_Op() : IMU_DATA size = {len(IMU_DATA.split(","))}')
#         if IMU_DATA and len(IMU_DATA.split(','))>=15:
#             if Flag:
#                 return 1
#             try:
#                 if writer==None:
#                     return -2
#                 print(IMU_DATA.split(','))
#                 a = ['IMU_DATA',*(list(map(float,IMU_DATA.split(','))))]
#                 writer.writerow(["IMU_DATA",*map(lambda x : float(x),IMU_DATA.split(','))])
#             except:gloabl IMU_Raw_Data
#                 print(IMU_DATA)


def IMU_Rx_Op():

    global IMU_Buf
    global IMU_Raw_Data
    global IMU_Rx_Data
    global IMU_Rx_Data_Byte
    global IMU_Data_Size

    IMU_Rx_Data = ""
    IMU_Buf = ""
    IMU_Rx_Data_Byte = ""
    IMU_Data_Size = 0
    print("IMU_Rx_Op()") # Debugging
    while True:
        while IMU_serial.inWaiting():

            IMU_Raw_Data = IMU_serial.read()
            print(IMU_Raw_Data)  # Debugging
            if IMU_Raw_Data != b'\r' and IMU_Raw_Data != b'\n':
                IMU_Buf += str(IMU_Raw_Data)  # buffering
                IMU_Buf = IMU_Buf.replace("'", "")  # remove (') and (b)
                IMU_Buf = IMU_Buf.replace("b", "")

                IMU_Rx_Queue.put(IMU_Buf)

            if (IMU_Raw_Data == b'\n' or IMU_Raw_Data == b'>') and IMU_Rx_Queue.qsize() > 1:
                for index in range(IMU_Rx_Queue.qsize()):
                    IMU_Rx_Data_Byte = IMU_Rx_Queue.get()

                    IMU_Rx_Data += IMU_Rx_Data_Byte

                return IMU_Rx_Data

            IMU_Buf = ""


def Get_Cfg_Data():
    global Received_IMU_Data
    Received_IMU_Data = ""

    while Received_IMU_Data != "pons:1":
        Received_IMU_Data = IMU_Rx_Op()
        print(Received_IMU_Data)
    return


def Get_IMU_Data():
    global Received_IMU_Data

    # print("Get IMU DATA")
    IMU_serial.write(b'*')
    Received_IMU_Data = IMU_Rx_Op()
    print(Received_IMU_Data)
    return Received_IMU_Data


def IMU_Init():

    print("IMU Init")

    global IMU_serial
    # connect ebimu
    IMU_serial = serial.Serial('/dev/ttyAMA1', 921600, parity='N',
                               timeout=0.001)  # when connect to GPIO pins (TX: GPIO 27, RX: GPIO 28)

    if IMU_serial.is_open:
        print("IMU OPEN")
    else:
        print("IMU NOT OPEN")


def IMU_Set_Baudrate(baudrate):
    global IMU_serial

    # when connect to GPIO pins (Tx: GPIO 27, Rx: GPIO 28)
    IMU_serial = serial.Serial('/dev/ttyAMA1', baudrate, parity='N', timeout=0.001)

    # when connect to USB (Windows)
    # IMU_serial = serial.Serial('COM5', baudrate, parity='N', timeout=0.001)


def IMU_Op(writer):
    global IMU_Data

    IMU_Data = Get_IMU_Data()

    if IMU_Data:

        try:
            # print(IMU_Data.split(','))
            # a = ['IMU_DATA', *(list(map(str, IMU_Data.split(','))))]
            writer.writerow(["IMU_DATA", *map(lambda x: str(x), IMU_Data.split(','))])  # IMU Data Logging

            # BT Operation
            ### can_Common.can_BT.Thread_Tx_Queue.put(IMU_Data.encode())

            return IMU_Data

        except:
            print(IMU_Data)

    else:
        return -1


if __name__ == "__main__":

    IMU_Init()

    while True:
        IMU_Op()
    # ----------------- For IMU Setting -----------------
'''
    IMU_reset() 
    IMU_Output_Rate_polling()

    IMU_Output_Code_ASCII()
    IMU_Output_Euler()

    IMU_Set_Acc_ON() # or IMU_Set_Velo_Local() / IMU_Set_Velo_Global()
    IMU_Set_Gyro_ON()
    IMU_Set_Temp_OFF()
    IMU_Set_Distance_Global()

    #IMU_921600()
    '''