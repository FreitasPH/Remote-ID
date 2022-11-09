#!/usr/bin/env python

import cmath
import rospy
from std_msgs.msg import String
from remoteid.msg import Drone_command, Coordinates


class Pilot:
    def __init__(self):
        self.keep_going = True
        self.droneid = "PR-202200001"

    def go(self):
        pub = rospy.Publisher('drone1_command', Drone_command, queue_size=10)
        pub_coor = rospy.Publisher('set1_coordinates', Coordinates, queue_size=10)
        rospy.init_node('Pilot1')
        rospy.Subscriber("storage_response", String, callback, self)
        freq = 1
        rate = rospy.Rate(freq)  # 1hz

        msg = Drone_command()
        coor = Coordinates()

        center = 1 + 1j
        pos = 2 + 2*1j

        angle = cmath.exp(1j * 2 * cmath.pi / 100)
        while not rospy.is_shutdown():

            msg.posx = int(pos.real*1000 + (-470886695))
            msg.posy = int(pos.imag*1000 + (-225911104))
            msg.posz = 0 + (30)

            coor.posx = pos.real
            coor.posy = pos.imag
            coor.posz = 0

            diff = pos-center
            diff *= angle
            pos = diff+center

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
