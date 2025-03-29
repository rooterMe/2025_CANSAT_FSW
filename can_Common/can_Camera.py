from picamera2 import Picamera2
import cs_Common.cs_BT
import cs_Common.cs_Time
from PIL import Image
import io
import base64
import os
import csv
import multiprocessing as mp

Thread_Encoding_Queue = mp.Queue()

global picamera0
global picamera1

def Is_Camera_Image_File(filename):

    if os.path.isfile(filename):
        return True

    else:
        return False


def Camera_SetUp(dirname):

    global picamera0
    global picamera1

    picamera0 = Picamera2(0)
    picamera1 = Picamera2(1)

    picamera0.configure(picamera0.create_preview_configuration())
    # picamera0.set_controls({"ExposureTime" : 50, "AnalogueGain" : 10})
    picamera1.configure(picamera1.create_preview_configuration())
    # picamera1.set_controls({"ExposureTime" : 50, "AnalogueGain" : 10})

    # camera0_config = picamera0.create_still_configuration(main={"size": (4608, 2592)}, lores={"size": (4608, 2592)}, display="lores")
    # camera1_config = picamera1.create_still_configuration(main={"size": (4608, 2592)}, lores={"size": (4608, 2592)}, display="lores")

    os.mkdir(dirname+"/Camera_Image")
    os.mkdir(dirname+"/Camera_Image/Camera_0")
    os.mkdir(dirname+"/Camera_Image/Camera_1")
    picamera0.start()
    picamera1.start()


def Cam0_Img_Cap(writer, path, name, Encode_Flag) :

    camera_filename = path+f'/Camera_Image/Camera_0/Camera0_{name}.jpg'

    try:   
        camera0_data = io.BytesIO()
        picamera0.capture_file(camera0_data, format='jpeg')

        camera0_image = Image.open(camera0_data)
        camera0_image.save(camera_filename)
        
        writer.writerow(["Picture", camera_filename])
        if Encode_Flag == True:
            Thread_Encoding_Queue.put([0,camera0_image])
            
    except Exception as e:
        print(f"[Error] {name} Cam0_Error : {e}")
        writer.writerow(["Picture", "Camera0 Error", e])
        

def Cam1_Img_Cap(writer, path, name, Encode_Flag):

    camera_filename = path+f'/Camera_Image/Camera_1/Camera1_{name}.jpg'

    try:
        camera1_data = io.BytesIO()
        picamera1.capture_file(camera1_data, format='jpeg')

        camera1_image = Image.open(camera1_data)
        camera1_image.save(camera_filename)
        
        writer.writerow(["Picture", camera_filename])
        if Encode_Flag == True:
            Thread_Encoding_Queue.put([1,camera1_image])
            
    except Exception as e:
        print(f"[Error] {name} Cam1_Error : {e}")
        writer.writerow(["Picture", "Camera1 Error", e])


def Encoding_Thread_Worker(Q):
    while True:
        while not Q.empty():
            index,image = Q.get()
            
            image = image.resize((160,120))
            
            resized_camera_data = io.BytesIO()
            image.save(resized_camera_data, 'jpeg')

            encoded_camera_data = base64.b64encode(resized_camera_data.getvalue())

            cs_Common.cs_BT.Thread_Tx_Queue.put(f'&{str(index)}'.encode()+encoded_camera_data)


def Camera_Op(writer, path, name, Encode_Flag): 
    print(f"Camera Operation {path, name}")
    Cam0_Img_Cap(writer, path, name, Encode_Flag)
    Cam1_Img_Cap(writer, path, name, Encode_Flag)


def Camera_Stop() :
    picamera0.stop()
    picamera1.stop()
