from picamera2 import Picamera2
import can_Common.can_BT
import can_Common.can_Time
from PIL import Image
import io
import base64
import os
import csv
import multiprocessing as mp

Thread_Encoding_Queue = mp.Queue()

global picamera0

def Is_Camera_Image_File(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False

def Camera_SetUp(dirname):
    global picamera0

    picamera0 = Picamera2(0)
    picamera0.configure(picamera0.create_preview_configuration())

    # Create Camera_Image directory
    os.mkdir(dirname + "/Camera_Image")
    picamera0.start()

def Cam0_Img_Cap(writer, path, name, Encode_Flag):
    camera_filename = path + f'/Camera_Image/Camera_{name}.jpg'

    try:
        camera0_data = io.BytesIO()
        picamera0.capture_file(camera0_data, format='jpeg')

        camera0_image = Image.open(camera0_data)
        camera0_image.save(camera_filename)
        
        writer.writerow(["Picture", camera_filename])
        if Encode_Flag:
            Thread_Encoding_Queue.put([0, camera0_image])
            
    except Exception as e:
        print(f"[Error] {name} Cam0_Error : {e}")
        writer.writerow(["Picture", "Camera0 Error", e])

def Encoding_Thread_Worker(Q):
    while True:
        while not Q.empty():
            index, image = Q.get()
            
            image = image.resize((160, 120))
            
            resized_camera_data = io.BytesIO()
            image.save(resized_camera_data, 'jpeg')

            encoded_camera_data = base64.b64encode(resized_camera_data.getvalue())

            # BT Operation
            ### can_Common.can_BT.Thread_Tx_Queue.put(f'&{str(index)}'.encode() + encoded_camera_data)

def Camera_Op(writer, path, name, Encode_Flag): 
    print(f"Camera Operation {path, name}")
    Cam0_Img_Cap(writer, path, name, Encode_Flag)

def Camera_Stop():
    picamera0.stop()