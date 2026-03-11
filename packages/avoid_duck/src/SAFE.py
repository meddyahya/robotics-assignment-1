#!/usr/bin/env python3 
import os
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import WheelsCmdStamped
from sensor_msgs.msg import Range

# min_range is 0.03m and max_range is 2.00m for the ToF sensor of Duckietown robots.
class ObstacleDetection(DTROS):
    def __init__(self, node_name):
        super(ObstacleDetection, self).__init__(
            node_name=node_name,
            node_type=NodeType.CONTROL
        )
        # rospy.init_node is handled by DTROS parent class
        self.distance_limit = 0.10 # 0.10 if unit in meters
        self.forward_speed = 0.2

        # both of the below publisher and subscriber have different
        # topics because each topic carries one type of information.

        host_name = os.environ['VEHICLE_NAME']
        wheels_topic = f"/{host_name}/wheels_driver_node/wheels_cmd"
        tof_topic = f"/{host_name}/front_center_tof_driver_node/range"

        
        self.publisher = rospy.Publisher( # from the program to the robot
            wheels_topic, # topic name. i need to change host name with robot's name
            WheelsCmdStamped, # message type
            queue_size=1
        )
        #rospy.sleep(1.0)
        rospy.Subscriber( # distance from sensor; from the robot to the program
            tof_topic, 
            Range,
            self.callback_tof
        )
        #rospy.sleep(1.0)

    def callback_tof(self, msg):# callback function for the ToF subscriber
        if msg.range < msg.min_range or msg.range > msg.max_range:
            return
        
        rospy.loginfo(f"ToF distance: {msg.range:.3f} m")

        if msg.range <= self.distance_limit:
            self.send_wheel_cmd(0.0, 0.0)
        else:
            self.send_wheel_cmd(self.forward_speed, self.forward_speed) # self.forward_speed, self.forward_speed)

    def send_wheel_cmd(self, vel_left, vel_right):
        msg = WheelsCmdStamped()
        msg.vel_left = vel_left
        msg.vel_right = vel_right
        self.publisher.publish(msg)


if __name__ == "__main__":
    node = ObstacleDetection(node_name="task3_node")
    rospy.spin()
