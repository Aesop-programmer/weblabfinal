#   Blackboard Note

## motivation



Many teachers like to teach with blackboard. However, it's tough for students to listen and take notes simultaneously. Therefore, we hope students can learn focusly with notes automatically recorded. 




## abstract
Blackboard Note讓使用者透過手持裝有九軸感測器的裝置進行書寫，達成同時將書寫文字記錄成電子形式的功能。

Blackboard Note let users can write by using mpu9250, making handwritten into digital stored data





## technique and hardware
technique:
- Python
- Arduino IDE
- MQTT

hardware:
- Jetson Nano
- ESP32
- MPU9250
  



## main structure
![image](https://user-images.githubusercontent.com/55504676/174087611-7db52f0f-6547-4480-80e8-043ad429385e.png)


## how to run

- install wi_senddata.ino on ESP32
- Install related python packages on Jetson Nano
```bash
$ python3 -m pip install -r requirements.txt
```
- Run the eclipse mosquitto docker container on Jetson Nano
```bash
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
- Run the IMUtrackingcode and publisher on Jetson Nano
```bash
$ python3 final_wif.py
```


- Install related python packages on pc
```bash
$ python3 -m pip install -r requirementsClient.txt
```
- Run the subscriber on pc to see motion
```bash
$ python3 subscriber.py --ip [jetson nano ip address] -- port 1883
```
## how to use
1. User take ESP32 to write
2. Push button to end writing
4. Watch handwritten on computer



## demo
https://www.youtube.com/watch?v=FaFhwM_qoy4
## reference
- https://github.com/johnnylord/eclipse-mosquitto
- https://github.com/LibofRelax/IMU-Position-Tracking


