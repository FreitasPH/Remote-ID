#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from remoteid.msg import Drone_command, Coordinates


class Pilot:
    def __init__(self):
        self.keep_going = True
        self.droneid = "PR-202200003"

    def go(self):
        pub = rospy.Publisher('drone2_command', Drone_command, queue_size=10)
        pub_coor = rospy.Publisher('set2_coordinates', Coordinates, queue_size=10)
        rospy.init_node('Pilot2')
        rospy.Subscriber("storage_response", String, callback, self)
        freq = 1
        time = 1.0/freq
        rate = rospy.Rate(freq)  # 1hz

        msg = Drone_command()
        coor = Coordinates()

        posx = 12
        posy = 12
        posz = 10
        velx = -1
        vely = -1
        velz = -1

        while not rospy.is_shutdown():

            msg.posx = int(posx*1000 + (-470886695))
            msg.posy = int(posy*1000 + (-225911104))
            msg.posz = int(posz + (30))

            coor.posx = posx
            coor.posy = posy
            coor.posz = posz

            posx += velx*time
            posy += vely*time
            posz += velz*time
            
            if(posx >= 11.999 or posx <= 2):
                velx *= -1

            if(posy >= 11.999 or posy <= 2):
                vely *= -1

            if(posz >= 9.999 or posz <= 0):
                velz *= -1

            rospy.loginfo(msg)
            pub.publish(msg)
            pub_coor.publish(coor)

            rate.sleep()

            if not self.keep_going:
                rospy.spin()

def callback(data, piloto):
    response = data.data.split()

    if(response[0] == piloto.droneid):
        if(response[1] == "stop" and piloto.keep_going):
            rospy.loginfo("Ordem de parada recebida")
            piloto.keep_going = False

        if(response[1] == "warning"):
            rospy.loginfo("Mensagem de aviso recebida")


if __name__ == '__main__':
    try:
        pilot = Pilot()
        pilot.go()
    except rospy.ROSInterruptException:
        pass
