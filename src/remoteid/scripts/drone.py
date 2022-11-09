#!/usr/bin/env python

import datetime
from threading import Lock
import numpy as np
import rospy
#from std_msgs.msg import String
from remoteid.msg import Drone_command, Drone_data_encoded


class Drone():
    def __init__(self):
        self.posx = 2*1000 + (-470886695)
        self.posy = 2*1000 + (-225911104)
        self.posz = 0 + (30)
        self.droneid = "PR-202200001"
        self.vel = 0

        rospy.init_node('drone1')

        rospy.Subscriber("drone1_command", Drone_command, callback, self)

    def broadcast(self):
        pub = rospy.Publisher('drone_info_encoded', Drone_data_encoded, queue_size=10)

        freq = 1
        time = 1.0/freq
        rate = rospy.Rate(freq)
        
        msg_encoded = Drone_data_encoded()
        msg_encoded.headerID = 0
        msg_encoded.ID_UAS_Type = int("0b00100010",2) #ID Type = 2, UAS Type = 2
        msg_encoded.UAS_ID = self.droneid.zfill(20)

        mutex = Lock() 
        pos = np.array([self.posx, self.posy])
        altitude = self.posz

        while not rospy.is_shutdown():


            posant = pos
            altant = altitude

            with mutex:
                latitude = int(self.posx)
                longitude = int(self.posy)
                altitude = int(self.posz)
                now = datetime.datetime.now()

            pos = np.array([self.posx, self.posy])
            self.vel = np.linalg.norm(pos-posant)/time
            
            hvel = np.linalg.norm(pos-posant)*0.011112/time
            vvel = (altitude - altant)/time

            if (pos[1] - posant[1]) == 0:
                adj = 0.0000000001
            else:
                adj = pos[1] - posant[1]

            direction = int(np.arctan((pos[0] - posant[0])/adj)*180/np.pi)

            if adj < 0:
                direction += 180
            elif pos[0] < posant[0]:
                direction += 360

            if direction < 180:
                msg_encoded.Track_Direction = direction
                directionbit = 0
            else:
                msg_encoded.Track_Direction = direction - 180
                directionbit = 1

            if hvel <= 225*0.25:
                msg_encoded.Speed = int(round(hvel/0.25))
                multiplierflag = 0
            elif hvel > 225*0.25 and hvel < 254.25:
                msg_encoded.Speed = int(round((hvel-225*0.25)/0.75))
                multiplierflag = 1
            else:
                msg_encoded.Speed = 254
                multiplierflag = 1

            flag = "0b001000" + str(directionbit) + str(multiplierflag)

            msg_encoded.Status_Flags = int(flag,2)
            msg_encoded.Vertical_Speed = int(vvel/0.5)
            msg_encoded.Latitude = latitude
            msg_encoded.Longitude = longitude
            msg_encoded.Pressure_Altitude = 0
            msg_encoded.Geodetic_Altitude = int((altitude + 1000)/0.5)
            msg_encoded.Height = 0

            msg_encoded.Hori_Vert_Accuracy = int("0b00110100",2)
            msg_encoded.Baro_Speed_Accuracy = int("0b01000010",2)

            ts = int((now.minute*60 + now.second + now.microsecond/1000000.0)*10)
            msg_encoded.TimeStamp = ts
            msg_encoded.TimeStamp_Accuracy = int("0b00000001",2)

            rospy.loginfo(msg_encoded)
            pub.publish(msg_encoded)

            rate.sleep()

def callback(data, dron0):
    dron0.posx = data.posx
    dron0.posy = data.posy
    dron0.posz = data.posz


if __name__ == '__main__':
    try:
        #drone()
        drone = Drone()
        drone.broadcast()
    except rospy.ROSInterruptException:
        pass
