#!/usr/bin/env python

import datetime
#from threading import Lock
import numpy as np
import rospy
#from std_msgs.msg import String
from remoteid.msg import Drone_command, Drone_data_encoded, Coordinates

class Drone:
    def __init__(self):
        self.posx = 12*1000 + (-470886695)
        self.posy = 12*1000 + (-225911104)
        self.posz = 10 + (30)
        self.droneid = "PR-202200002"
        self.vel = 0

        rospy.init_node('drone2')

        rospy.Subscriber("drone2_command", Drone_command, callback, self)

    def broadcast(self):
        pub = rospy.Publisher('drone2_info_encoded', Drone_data_encoded, queue_size=10)
        pub_coor = rospy.Publisher('set3_coordinates', Coordinates, queue_size=10)
        freq = 1
        time = 1.0/freq
        rate = rospy.Rate(freq)  # 1hz

        coor = Coordinates()

        msg_encoded = Drone_data_encoded()
        msg_encoded.headerID = 0
        msg_encoded.ID_UAS_Type = int("0b00100010",2) #ID Type = 2, UAS Type = 2
        msg_encoded.UAS_ID = self.droneid.zfill(20)


        posx = 13
        posy = 13
        posz = 14
        hvel = 0
        
        velx = 1.0
        vely = 2.0
        velz = 1.0

        while not rospy.is_shutdown():
            coor.posx = posx
            coor.posy = posy
            coor.posz = posz

            latitude = int(posx*1000 + (-470886695))
            longitude = int(posy*1000 + (-225911104))
            altitude = int(posz + (30))
            now = datetime.datetime.now()

            posx += velx*time
            posy += vely*time
            posz += velz*time

            hvel = np.linalg.norm(np.array([velx, vely]))*11.112/time
            vvel = velz

            if (vely) == 0:
                adj = 0.0000000001
            else:
                adj = vely

            direction = int(np.arctan((velx)/adj)*180/np.pi)

            if adj < 0:
                direction += 180
            elif velx < 0:
                direction += 360

            if(posx >= 17.999 or posx <= 13):
                velx *= -1

            if(posy >= 22.999 or posy <= 13):
                vely *= -1

            if(posz >= 18.999 or posz <= 14):
                velz *= -1

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
            pub_coor.publish(coor)

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
