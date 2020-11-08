#!/usr/bin/env python3
import numpy as np
import os
import rospy
from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from duckietown_msgs.msg import Twist2DStamped, WheelEncoderStamped, WheelsCmdStamped
from std_msgs.msg import Header, Float32
import rosbag
import math

class MyOdometryNode(DTROS):

    def __init__(self, node_name, _radius_flag):
        """Wheel Encoder Node
        This implements basic functionality with the wheel encoders.
        """

        # Initialize the DTROS parent class
        super(MyOdometryNode, self).__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        self.veh_name = rospy.get_namespace().strip("/")

        # Get static parameters
#         self._radius = rospy.get_param(f'/{self.veh_name}/kinematics_node/radius', 100)
        self._radius = rospy.get_param('~radius',50)
        # self._radius = 0.0318

        # Subscribing to the wheel encoders
        self.sub_encoder_ticks_left = rospy.Subscriber('/jcdgo/left_wheel_encoder_node/tick', WheelEncoderStamped,
                                                       self.left_encoder_data, queue_size=1)
        self.sub_encoder_ticks_right = rospy.Subscriber('/jcdgo/right_wheel_encoder_node/tick', WheelEncoderStamped,
                                                        self.right_encoder_data, queue_size=1)
        self.sub_executed_commands = rospy.Subscriber('/jcdgo/wheels_driver_node/wheels_cmd', WheelsCmdStamped,
                                                      self.cb_executed_cmds, queue_size=1)

        # Publishers (for exe28)
        self.pub_integrated_distance_left = rospy.Publisher('/jcdgo/my_left_travel_dist', Float32)
        self.pub_integrated_distance_right = rospy.Publisher('/jcdgo/my_right_travel_dist',Float32)

        self.Ntotal = 135
        self.Nticks_left_delta = 0
        self.Nticks_left_last = 0
        self.Nticks_left_accum = 0

        self.Nticks_right_delta = 0
        self.Nticks_right_last = 0
        self.Nticks_right_accum = 0

        self.iter_left = 0
        self.iter_right = 0

        self.left_travel_dist_accum=0
        self.right_travel_dist_accum=0
        # self.iter_wheel_cmd = 0
        self._radius_cali = _radius_flag
        self.vel_left = 0
        self.vel_right = 0

        self.log("Initialized")
        # create bag files:
        # self.bag = bag


    def cb_executed_cmds(self, msg):
        """ Use the executed commands to determine the direction of travel of each wheel.
        """
        print("In wheels_cmd: recieved: ",msg.vel_left, msg.vel_right)
        self.vel_left = msg.vel_left
        self.vel_right = msg.vel_right


    def left_encoder_data(self,data):
        rospy.loginfo("In left_encoder_data: recieved: " + str(data.data))
        if self.iter_left ==0:
            self.Nticks_left_last = data.data
        else:
            self.Nticks_left_delta =  data.data - self.Nticks_left_last
            self.Nticks_left_last = data.data
            if self.vel_left <  0:
                self.Nticks_left_delta *= -1
            self.Nticks_left_accum += self.Nticks_left_delta

            # calculate distance
            print("Nticks_left_accum is: ", self.Nticks_left_accum)
            self.left_travel_dist_accum = self.Nticks_left_accum * 2 * self._radius * math.pi / self.Ntotal
            print("traveled dist: left:", self.left_travel_dist_accum)
            self.pub_integrated_distance_left.publish(self.left_travel_dist_accum)

            if self.Nticks_left_accum !=0:
                _radius_cali_left = self.Ntotal * self.left_travel_dist_accum / (2 * math.pi * self.Nticks_left_accum)
                print("current radius left:", _radius_cali_left)

        self.iter_left +=1


    def right_encoder_data(self,data):
        rospy.loginfo("In right_encoder_data: recieved: " + str(data.data))
        if self.iter_right ==0:
            self.Nticks_right_last = data.data
        else:
            self.Nticks_right_delta =  data.data - self.Nticks_right_last
            self.Nticks_right_last = data.data
            if self.vel_right <  0:
                self.Nticks_right_delta *= -1
            self.Nticks_right_accum += self.Nticks_right_delta

            # calculate distance
            print("Nticks_right_accum is: ", self.Nticks_right_accum)
            self.right_travel_dist_accum = self.Nticks_right_accum * 2 * self._radius * math.pi / self.Ntotal
            print("traveled dist: right:", self.right_travel_dist_accum)
            self.pub_integrated_distance_right.publish(self.right_travel_dist_accum)
            if self.Nticks_right_accum !=0:
                _radius_cali_right = self.Ntotal * self.right_travel_dist_accum / (2 * math.pi * self.Nticks_right_accum)
                print("current radius right:", _radius_cali_right)

        self.iter_right +=1




if __name__ == '__main__':
    # _radius_flag  = False
    _radius_flag  = True
    node = MyOdometryNode(node_name='my_odometry_node', _radius_flag=_radius_flag)

    # Keep it spinning to keep the node alive
    rospy.spin()
    rospy.loginfo("wheel_encoder_node is up and running...")