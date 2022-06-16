import socket
import serial
import numpy as np
from numpy.linalg import inv, norm

import data_receiver
from mathlib import *
from main import *
import time
import os.path
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

##############MQTT##############
import io
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect(host='localhost', port=1883)
client.loop_start()
################################

# bind all IP
HOST = '0.0.0.0'
# Listen on Port
PORT = 44444
# Size of receive buffer
BUFFER_SIZE = 1024
# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the host and port
s.bind((HOST, PORT))

'''
一開始沒通為輸出a 當通時開始讀資料
'''
time_start = time.time()

#ser = serial.Serial('COM3', baudrate=19200)
while True:
    # line = ser.readline()
    data = s.recvfrom(BUFFER_SIZE)
    if (data):
        # if line != b'':
        get_cm = str(data[0], 'utf-8')
        print('1', get_cm)
        if get_cm != 'off\n':
            break
f_xyz = open('xyz3.txt', 'w')
while True and get_cm != 'off\n':
    #line = ser.readline()
    if data:
        # get_cm = str(line).split("'")[1].split("\\")[0]
        get_cm = str(data[0], 'utf-8')
        print('2', get_cm)
        f_xyz.write(get_cm)
    data = s.recvfrom(BUFFER_SIZE)
    get_cm = str(data[0], 'utf-8')
f_xyz.close()

'''
算init
'''
f_xyz = open('xyz3.txt', 'r')
data_1 = []
for line in f_xyz.readlines():
    a = line.split(',')
    if(len(a) == 3):
        a[-1] = a[-1][0:-1]
        a = [1, 1, 1, a[0], a[1], a[2], 1, 1, 1]
        data_1.append(a)
f_xyz.close()
data = np.array(data_1, dtype=np.float64)
tracker = IMUTracker(sampling=83)
init_list = tracker.initialize(data[5:])


'''
第一次處理數據計算位置
'''
print('a')
f_xyz = open('xyz3.txt', 'w')
while True:
    state = False
    data = s.recvfrom(BUFFER_SIZE)
    while data and str(data[0], 'utf-8') != 'off\n':
        get_cm = str(data[0], 'utf-8')
        print(get_cm)
        f_xyz.writelines(get_cm)
        while (s.recvfrom(BUFFER_SIZE)):
            data = s.recvfrom(BUFFER_SIZE)
        # get_cm = str(line).split("'")[1].split("\\")[0]
            get_cm = str(data[0], 'utf-8')
            if(get_cm == 'off\n'):
                break
        state = True
    if state:
        break
f_xyz.close()

f_xyz = open('xyz3.txt', 'r')
data_1 = []
for line in f_xyz.readlines():
    a = line.split(',')
    if(len(a) == 3):
        a[-1] = a[-1][0:-1]
        a = [1, 1, 1, a[0], a[1], a[2], 1, 1, 1]
        data_1.append(a)
f_xyz.close()
data = np.array(data_1, dtype=np.float64)
a_nav, orix, oriy, oriz = tracker.attitudeTrack(
    data[1:], init_list)
a_nav_filtered = tracker.removeAccErr(a_nav, filter=False)
v = tracker.zupt(a_nav_filtered, threshold=0.2)
p = tracker.positionTrack(a_nav_filtered, v)
f_plot = open("xyz_plot.txt", "w")
p.tolist()

p_final = p[-1]

for j in range(len(p)):
    f_plot.write(str(p[j][0])+","+str(p[j][1])+","+str(p[j][2])+"\n")
f_plot.close()
'''
第一次畫圖
'''
'''
ax = plt.axes(projection='3d')
'''
print('aaaaaaa')
ax = plt.axes()
plt.xlim(-0.5, 0.5)
plt.ylim(-0.5, 0.5)
plt.grid(True)
#plt.ion()
x = list()
y = list()
z = list()
f_plot = open('xyz_plot.txt', 'r')

for line in f_plot.readlines()[:-1]:
    a = line.split(',')
    a[-1] = a[-1][0:-1]
    x.append(np.float64(a[0]))
    y.append(np.float64(a[1]))
    z.append(np.float64(a[2]))
    '''
    value = 4*(max(max(x), max(y), max(z)))
    value = range(-abs(int(value)), abs(int(value)), 10)
    
    ax.set_xticks(value)
    ax.set_yticks(value)
    '''

    ax.plot(x, y, 'blue')
    #plt.pause(0.01)
fio = io.BytesIO()
plt.savefig(fio, format='png')
plt.savefig('first.png')
fio.seek(0)
byteArr = bytearray(fio.read())
client.publish(topic="png", payload=byteArr)

f_plot.close()
'''
plt.close()
'''
'''
之後的迴圈 off 會甚麼都不做   state 為True時 表示要算 False為off的狀態
'''
state = False

while True:
    time_end = time.time()
    if(time_end - time_start > 120):
        plt.close()
        break
    
    
    data = s.recvfrom(BUFFER_SIZE)
    if data and str(data[0], 'utf-8') != 'off\n':
        f_xyz = open('xyz3.txt', 'w')
    while data and str(data[0], 'utf-8') != 'off\n':
        get_cm = str(data[0], 'utf-8')
        print(get_cm)
        f_xyz.writelines(get_cm)
        while (s.recvfrom(BUFFER_SIZE)):
            data = s.recvfrom(BUFFER_SIZE)
        # get_cm = str(line).split("'")[1].split("\\")[0]
            get_cm = str(data[0], 'utf-8')
            if(get_cm == 'off\n'):
                break
        state = True
    if state:
        f_xyz.close()
        f_xyz = open('xyz3.txt', 'r')
        data_1 = []
        for line in f_xyz.readlines():
            a = line.split(',')
            if(len(a) == 3):
                a[-1] = a[-1][0:-1]
                a = [1, 1, 1, a[0], a[1], a[2], 1, 1, 1]
                data_1.append(a)
        f_xyz.close()
        data = np.array(data_1, dtype=np.float64)
        a_nav, orix, oriy, oriz = tracker.attitudeTrack(
            data[0:], init_list)
        a_nav_filtered = tracker.removeAccErr(a_nav, filter=False)
        v = tracker.zupt(a_nav_filtered, threshold=0.2)
        p = tracker.positionTrack(a_nav_filtered, v)
        for position in p:
            position[0] = p_final[0] + position[0]
            position[1] = p_final[1] + position[1]
            position[2] = p_final[2] + position[2]
        p_final = p[-1]
        f_plot = open('xyz_plot.txt', "w")
        p.tolist()
        for j in range(len(p)):
            f_plot.write(str(p[j][0])+","+str(p[j][1])+","+str(p[j][2])+"\n")
        f_plot.close()

        f_plot = open('xyz_plot.txt', 'r')
        for line in f_plot.readlines()[:-1]:
            a = line.split(',')
            a[-1] = a[-1][0:-1]
            x.append(np.float64(a[0]))
            y.append(np.float64(a[1]))
            z.append(np.float64(a[2]))
            '''
            value = 4*(max(max(x), max(y), max(z)))
            value = range(-abs(int(value)), abs(int(value)), 10)
            ax.set_xticks(value)
            ax.set_yticks(value)
            '''
            ax.plot(x, y, 'blue')
        # fio = io.BytesIO()
        # plt.savefig(fio, format='png')
        # plt.savefig('trytry.png')
        # print('bbbb')
        # byteArr = bytearray(fio.read())
        # fio.seek(0)
        # client.publish(topic="png", payload=byteArr)
            #plt.pause(0.01)
        # plt.savefig('2D.png')
        plt.savefig('tmp.png', format='png')
        f=open("tmp.png", 'rb')
        # print(type(buf))
        byteArr = bytearray(f.read())
        # Publish the message to topic
        client.publish(topic="png", payload=byteArr)
        f.close()
        print('end')
        state = False
        f_plot.close()
        '''
        plt.close()
        '''
