#!/usr/bin/env python
import datetime
import pytz
import rospy
#from std_msgs.msg import String
from remoteid.msg import Drone_data_encoded, Drone_data_decoded


def callback(data):
    #rospy.loginfo("I received the message: %s", data.data)

    now = datetime.datetime.now(pytz.timezone('Brazil/East'))
    msg = Drone_data_decoded()

    ID_UAS_Type_binary = format(data.ID_UAS_Type, '08b')
    msg.ID_Type = int(ID_UAS_Type_binary[0:4], 2)
    msg.UAS_Type = int(ID_UAS_Type_binary[4:8], 2)
    msg.UAS_ID = data.UAS_ID.strip("0")

    Status_Flags_binary = format(data.Status_Flags, '08b')
    msg.Status =  int(Status_Flags_binary[0:4], 2)
    #Height_Type = Status_Flags_binary[5]
    directionbit = Status_Flags_binary[6]
    multiplierflag = Status_Flags_binary[7]

    msg.Direction = data.Track_Direction
    if directionbit == "1":
        msg.Direction += 180

    if multiplierflag == "0":  
        msg.Speed = data.Speed * 0.25
    else:
        msg.Speed = data.Speed * 0.75 + (255*0.25)

    msg.Vertical_Speed = data.Vertical_Speed * 0.5
    msg.Latitude = data.Latitude/10000000.0
    msg.Longitude = data.Longitude/10000000.0
    msg.Geodetic_Altitude = (data.Geodetic_Altitude*0.5) - 1000

    Hori_Vert_Accuracy_binary = format(data.Hori_Vert_Accuracy, '08b')
    msg.Vertical_Accuracy = int(Hori_Vert_Accuracy_binary[0:4],2)
    msg.Horizontal_Accuracy = int(Hori_Vert_Accuracy_binary[4:8],2)

    Baro_Speed_Accuracy_binary = format(data.Baro_Speed_Accuracy, '08b')
    msg.Altitude_Accuracy = int(Baro_Speed_Accuracy_binary[0:4],2)
    msg.Speed_Accuracy = int(Baro_Speed_Accuracy_binary[4:8],2)

    TimeStamp_minute = data.TimeStamp//600
    Time_Stamp_second = (data.TimeStamp%600)//10
    Time_Stamp_microsecond = (data.TimeStamp%600)%10*100000
    if data.TimeStamp > int((now.minute*60 + now.second + now.microsecond/1000000.0)*10):
        Timestamp = now.replace(hour = now.hour-1, minute = TimeStamp_minute, second = Time_Stamp_second, microsecond= Time_Stamp_microsecond)
    else:
        Timestamp = now.replace(minute = TimeStamp_minute, second = Time_Stamp_second, microsecond= Time_Stamp_microsecond)
    msg.TimeStamp = str(Timestamp)
    TimeStamp_Accuracy_binary = format(data.TimeStamp_Accuracy, '08b')
    msg.TimeStamp_Accuracy = int(TimeStamp_Accuracy_binary[4:8],2)*0.1

    #rospy.loginfo("Received: ID: %d, Pos: (%.2f,%.2f,%.2f), Vel: %.2f, Time: %s" % (data.id, data.posx, data.posy, data.posz, data.vel, data.time))

    rospy.loginfo(msg)
    pub = rospy.Publisher("storage_info", Drone_data_decoded, queue_size=10)
    pub.publish(msg)


def ground():

    rospy.init_node('Observador2')

    rospy.Subscriber("drone_info_encoded_2", Drone_data_encoded, callback)
    
    rospy.spin()


if __name__ == '__main__':
    ground()
