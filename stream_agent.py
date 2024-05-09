# Copyright (c) 2024, OPENZEKA.  All rights reserved.

from client_se import ClientSE
import time
import argparse

parser = argparse.ArgumentParser(description='Please provide the Target IP, Stream Engine Port and Token')
parser.add_argument('--target_ip', type=str,
                    help='Target IP Address of the device with Cordatus Stream Engine')
parser.add_argument('--target_port', type=int,
                    help='Port of the Cordatus Stream Engine running on the target device')
parser.add_argument('--token', type=str,
                    help='Token of the running Cordatus Client instance on the target device')
args = parser.parse_args()

# target_ip = "http://192.168.1.230:7005"
target_ip = "http://" + args.target_ip + ":" + str(args.target_port)
token = args.token

client = ClientSE(target_ip, token)
ret, msg = client.check()
print(msg)

if not ret:
    print("Unauthorized")
    exit()

# Open Local/Remote USB Camera
client.open_usb("video0", width=1280, height=960, fps=30)

# Open Local/Remote CSI Camera
# client.open_csi("video0", sensor_mode=4, width=1280, height=720, fps=30)

# Open Local/Remote IP Camera (HTTP - Public)
# client.open_ip("http://renzo.dyndns.tv/mjpg/video.mjpg")

# Open Local/Remote IP Camera (RTSP - Hikvision)
# client.open_ip("rtsp://Username:Password@<cam_ip_address>:554/cam/realmonitor?channel=1/subtype=0")

client.run()
time.sleep(3)
counter = 0

while True:
    ret, frame = client.read()
    if ret:
        counter += 1
        print(counter, frame.shape)
        time.sleep(1/30)
    
    if counter > 1000:
        break

client.close()