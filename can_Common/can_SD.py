import csv
import os

##########################
# We Don't use this file #
##########################

'''
FileTime = cs_Time.Time_Return()
FilePath = "Cansat_Log/cs_Log/"
FileName = f"{FilePath}CANSAT_LOG_{FileTime}.csv"

global CANSAT_LOG
global CANSAT_Logger

CANSAT_Logger = csv.writer(CANSAT_LOG)

def SD_LOG_MAKE_FILE(time) :
    path = "./" + f"cansat_test_{time}"
    os.mkdir(path)

def SD_LOG_FILE_OPEN() :
    try:
        CANSAT_LOG = open(FileName, 'w')

    except:
        print("Failed to open file")

def SD_LOG_Op(macData) : # TODO : LOG OPERATION 함수 구현 필요
    CANSAT_Logger.writerow(macData)

'''


