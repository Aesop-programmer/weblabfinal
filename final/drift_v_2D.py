
from matplotlib import projections
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
import matplotlib.pyplot as plt
import numpy as np

'''
一開始沒通為輸出a 當通時開始讀資料
'''
time_start = time.time()

ser = serial.Serial('/dev/ttyUSB0', baudrate=19200)
while True:
    line = ser.readline()
    if line != b'':
        get_cm = str(line).split("'")[1].split("\\")[0]
    print("get_cm:", get_cm)
    if get_cm != 'off':
        break
f_xyz = open('xyz3.txt', 'w')
i = 0
while True and get_cm != 'off':
    line = ser.readline().decode()
    print("line:", line)
    get_cm = str(line).split("'")[1].split("\\")[0]
    print("get_cm:", get_cm)
    f_xyz.writelines(get_cm+"\n")
f_xyz.close()
'''
算init
'''
f_xyz = open('xyz3.txt', 'r')
data_1 = []
for line in f_xyz.readlines():
    a = line.split(',')
    if(len(a) == 9):
        a[-1] = a[-1][0:-1]
        a[0] = 0
        a[1] = 0
        a[2] = 0
        data_1.append(a)
        b = [a[-3], a[-2], a[-1]]
f_xyz.close()
data = np.array(data_1, dtype=np.float64)
tracker = IMUTracker(sampling=83)
init_list = tracker.initialize(data[5:49])


'''
第一次處理數據計算位置
'''
f_xyz = open('xyz3.txt', 'w')
while True:
    state = False
    while str(ser.readline()).split("'")[1].split("\\")[0] != 'off':
        line = ser.readline()
        get_cm = str(line).split("'")[1].split("\\")[0]
        print('input_inf: ', get_cm)
        f_xyz.writelines(get_cm+"\n")
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
        a = [0, 0, 0, a[0], a[1], a[2], b[0], b[1], b[2]]
        data_1.append(a)
f_xyz.close()
data = np.array(data_1, dtype=np.float64)
a_nav, orix, oriy, oriz = tracker.attitudeTrack(
    data[5:], init_list)
a_nav_filtered = tracker.removeAccErr(a_nav, filter=True)
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
ax = plt.axes()
plt.xlim(-0.5, 0.5)
plt.ylim(-0.5, 0.5)
plt.grid(True)
plt.ion()
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

    ax.scatter(x, y, c='blue', s=0.1)
    plt.pause(0.01)
plt.savefig('2D.png')
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
    f_xyz = open('xyz3.txt', 'w')
    while str(ser.readline()).split("'")[1].split("\\")[0] != 'off':
        line = ser.readline()
        get_cm = str(line).split("'")[1].split("\\")[0]
        print('input_inf: ', get_cm)
        f_xyz.writelines(get_cm+"\n")
        state = True
    f_xyz.close()
    if state:
        f_xyz = open('xyz3.txt', 'r')
        data_1 = []
        for line in f_xyz.readlines():
            a = line.split(',')
            if(len(a) == 3):
                a[-1] = a[-1][0:-1]
                a = [0, 0, 0, a[0], a[1], a[2], b[0], b[1], b[2]]
                data_1.append(a)
        f_xyz.close()
        data = np.array(data_1, dtype=np.float64)
        a_nav, orix, oriy, oriz = tracker.attitudeTrack(
            data[5:], init_list)
        a_nav_filtered = tracker.removeAccErr(a_nav, filter=True)
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
            ax.scatter(x, y, c='blue', s=0.1)
            plt.pause(0.01)
        plt.savefig('2D.png')
        print('end')
        state = False
        f_plot.close()
        '''
        plt.close()
        '''
