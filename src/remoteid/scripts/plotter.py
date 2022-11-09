#!/usr/bin/env python

import matplotlib.pyplot as plt
import rospy
#import numpy as np
from matplotlib.animation import FuncAnimation
from remoteid.msg import Coordinates
from mpl_toolkits.mplot3d import Axes3D

class Visualiser:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        self.ln, = self.ax.plot([], [], [], 'b-')
        self.ln2, = self.ax.plot([], [], [], 'g-')
        self.ln3, = self.ax.plot([], [], [], 'r-.')
        self.pt1, = self.ax.plot([], [], [], 'kx')
        self.pt2, = self.ax.plot([], [], [], 'kx')
        self.pt3, = self.ax.plot([], [], [], 'kx')
        self.x_data1, self.y_data1, self.z_data1 = [] , [] , []
        self.x_last1, self.y_last1, self.z_last1 = [] , [] , []
        self.x_data2, self.y_data2, self.z_data2 = [] , [] , []
        self.x_last2, self.y_last2, self.z_last2 = [] , [] , []
        self.x_data3, self.y_data3, self.z_data3 = [] , [] , []
        self.x_last3, self.y_last3, self.z_last3 = [] , [] , []

        self.patches = [self.ln, self.ln2, self.ln3, self.pt1]

    def plot_init(self):
        self.ax.set_xlim(-4, 25)
        self.ax.set_ylim(-4, 25)
        self.ax.set_zlim(-4, 25)
        self.ax.set_xlabel("Latitude")
        self.ax.set_ylabel("Longitude")
        self.ax.set_zlabel("Altitude")
        return self.patches

    def callback1(self, msg):
        self.z_data1.append(msg.posz)
        self.y_data1.append(msg.posy)
        self.x_data1.append(msg.posx)

        self.x_last1 = [msg.posx]
        self.y_last1 = [msg.posy]
        self.z_last1 = [msg.posz]

    def callback2(self, msg):
        self.z_data2.append(msg.posz)
        self.y_data2.append(msg.posy)
        self.x_data2.append(msg.posx)

        self.x_last2 = [msg.posx]
        self.y_last2 = [msg.posy]
        self.z_last2 = [msg.posz]

    def callback3(self, msg):
        self.z_data3.append(msg.posz)
        self.y_data3.append(msg.posy)
        self.x_data3.append(msg.posx)

        self.x_last3 = [msg.posx]
        self.y_last3 = [msg.posy]
        self.z_last3 = [msg.posz]
    
    def update_plot(self, frame):
        self.ln.set_data(self.x_data1, self.y_data1)
        self.ln.set_3d_properties(self.z_data1)

        self.pt1.set_data(self.x_last1, self.y_last1)
        self.pt1.set_3d_properties(self.z_last1)

        self.ln2.set_data(self.x_data2, self.y_data2)
        self.ln2.set_3d_properties(self.z_data2)

        self.pt2.set_data(self.x_last2, self.y_last2)
        self.pt2.set_3d_properties(self.z_last2)

        self.ln3.set_data(self.x_data3, self.y_data3)
        self.ln3.set_3d_properties(self.z_data3)

        self.pt3.set_data(self.x_last3, self.y_last3)
        self.pt3.set_3d_properties(self.z_last3)

        return self.patches


rospy.init_node('visual_node')
vis = Visualiser()
rospy.Subscriber('set1_coordinates', Coordinates, vis.callback1)
rospy.Subscriber('set2_coordinates', Coordinates, vis.callback2)
rospy.Subscriber('set3_coordinates', Coordinates, vis.callback3)

ani = FuncAnimation(vis.fig, vis.update_plot, init_func=vis.plot_init)
plt.show(block=True) 