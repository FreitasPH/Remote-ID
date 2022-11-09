#!/usr/bin/env python
import sqlite3
from sqlite3 import Error
#import datetime
#from datetime import datetime
import rospy
from std_msgs.msg import String
from remoteid.msg import Drone_data_decoded

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
    except Error as e:
        print(e)

    return conn

def callback(data, args):
    conn = args[0]
    stop = args[1]

    print("\n")
    rospy.loginfo(data)
    print("\n")

    pub = rospy.Publisher('storage_response', String, queue_size=10)

    cur = conn.cursor()
    cur.execute("""select * from volumes 
                    where latmin <= ? and latmax >= ?
                    and lonmin <= ? and lonmax >= ?
                    and altmin <= ? and altmax >= ?
                    and tmin <= ? and tmax >= ?;""" ,
                    (data.Latitude, data.Latitude, data.Longitude, data.Longitude, data.Geodetic_Altitude, data.Geodetic_Altitude, data.TimeStamp, data.TimeStamp,))

    rows = cur.fetchall()

    if rows:
        
        for row in rows:
            if (row[0] == data.UAS_ID):
                rospy.loginfo("Drone ID: %s: OK" % (data.UAS_ID))
            else:
                rospy.loginfo("Drone ID: %s: Invadindo volume reservado para drone ID: %s" % (data.UAS_ID, row[0]))
                stop_command = "%s stop" % (data.UAS_ID)
                pub.publish(stop_command)
                if data.UAS_ID in stop:
                    stop[data.UAS_ID] += 1
                else:
                    stop[data.UAS_ID] = 1

                if stop[data.UAS_ID] >= 3 and data.Speed >= 0.000001:
                    stop_command = "%s stop" % (row[0])
                    rospy.loginfo("Drone ID: %s nao parou, drone ID: %s deve parar" % (data.UAS_ID, row[0]))
                    pub.publish(stop_command)
    
    else:
        rospy.loginfo("Drone ID: %s: Voando fora do volume reservado" % (data.UAS_ID))
        warning = "%s warning" % (data.UAS_ID)
        pub.publish(warning)


def USS():

    rospy.init_node('USS')

    conn = create_connection(r"/home/user/catkin_ws/src/remoteid/db/volumes.db")

    stop = {}

    rospy.Subscriber("storage_info", Drone_data_decoded, callback, (conn, stop))

    rospy.spin()


if __name__ == '__main__':
    USS()