# Cordatus Stream Engine - Live Stream Agent
This agent enables our users to benefit from Cordatus Stream Engine's low latency hardware accelerated live camera streaming capabilities for custom AI applications. 

Agent is designed and tested to work with local camera sources including USB, CSI and RTSP/HTTP but it can also be used if the remote client necessary ports are forwarded accordingly.

## Custom Code Integration
In order to work with physical cameras using this agent, Cordatus Client needs to be up and running on the target device with the source is attached. For RTSP/HTTP sources, at least one of the main-stream or sub-stream needs to be accessible within the same network. You can test RTSP/HTTP stream availablity by using VLC Media Player prior to this agent.

![RTSP Stream Test Sample](/assets/vlc_hikvision_cam.png)

If Cordatus Client is already running, the Cordatus Stream Engine should be available on port 7005 by default if it is not already occupied by some other application or service.

You can always check the port of the Cordatus Stream Engine service via the following terminal command:
```
ps -ef | grep cordatus_se
```
![Service Port](/assets/cse_port.png)

### Defining the Target and Initializing the ClientSE
First, we will start by gathering the IP address, port and token arguments via the terminal command and initialize the ClientSE class:
```
client = ClientSE(target_ip, token)
ret, msg = client.check()
print(msg)

if not ret:
    print("Unauthorized")
    exit()
```

If the token is wrong, the script will throw `Unauthorized` error.

### Camera Function Calls
Then we need to specify which function should be used to open the local/remote camera stream by uncommenting one of the appropriate function calls provided.
```
# Open Local/Remote USB Camera
client.open_usb("video0", width=1280, height=960, fps=30)
```
```
# Open Local/Remote CSI Camera
client.open_csi("video0", sensor_mode=4, width=1280, height=720, fps=30)
```
```
# Open Local/Remote IP Camera (HTTP - Public)
client.open_ip("http://renzo.dyndns.tv/mjpg/video.mjpg")
```
```
# Open Local/Remote IP Camera (RTSP - Hikvision)
client.open_ip("rtsp://Username:Password@<cam_ip_address>:554/cam/realmonitor?channel=1/subtype=0")
```

### Establishing Connection and Opening the Camera
In order to establish the connection between the local/remote target device and open the camera source, the `run()` function will be called. We will be receiving the frames via the `read()` function call inside an infinite `while` loop:
```
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
```
### Integrating Custom Code
Within the `while` loop, you can place your code blocks to work with the frame you receive from Cordatus Stream Engine. The `frame` variable is the Numpy array in RGB format.

## Building the Project Locally
Depending on the Python version that your project requires, build the sample image by providing the version information as follows:
```
./build_locally.sh 3.8

or

./build_locally.sh 3.11
```
To run the container on x86 platforms:
```
xhost + && docker run -ti --gpus=all --network=host --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY cordatus-live-stream-agent:v1.0-x86-py3.8.19

or

xhost + && docker run -ti --gpus=all --network=host --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY cordatus-live-stream-agent:v1.0-x86-py3.11.9
```

To run the container on NVIDIA Jetson platforms:
```
xhost + && docker run -ti --runtime=nvidia --network=host --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY cordatus-live-stream-agent:v1.0-aarch64-py3.8.19

or

xhost + && docker run -ti --runtime=nvidia --network=host --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY cordatus-live-stream-agent:v1.0-aarch64-py3.11.9
```

## Get Your Cordatus AI Token
Navigate to the https://cordatus.ai and login to your account. Under the Devices tab, click on the `Actions` button of the target device and select `Generate Token`. This screen will provide you the necessary token information.

![Retrieve your token](/assets/retrieve_token.gif)

## Running the Code
```
python3 stream_agent.py --target_ip 192.168.1.230 --target_port 7005 --token 7mXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXm3sh9V
```

## TODOs
- [ ] Content will be extended to demonstrate sample computer vision applications.
- [ ] New GPU accelerated base Docker images will be added from nvcr.io
