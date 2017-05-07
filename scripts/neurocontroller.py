#!/usr/bin/env python

import rospy
import numpy
import math

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Range
from nav_msgs.msg import Odometry

from ros_stdr_ga.srv import *

from pybrain.structure import FeedForwardNetwork, SigmoidLayer, LinearLayer, FullConnection
from pybrain.tools.shortcuts import buildNetwork

from pybrain.tools.xml.networkwriter import NetworkWriter

from subprocess import call


# Parameters
N_SONAR = 4 # Number of sonars in the robot

LINEAR_MUL = 2 # Used to denormalize ANN output
ANGULAR_MUL = 2

ranges = [0] * N_SONAR
odom = [0] * 2

ann = 0

def callbackSonar(msg, arg):
	#rospy.loginfo("%f: [%f]"%(arg, msg.range))
	if msg.range == float("inf"):
		msg.range = msg.max_range

	ranges[arg] = msg.max_range / msg.range # Normalize ranges, needed to feed the ANN

def callbackOdom(msg):
	odom[0] = msg.pose.pose.position.x
	odom[1] = msg.pose.pose.position.y

def initANN():
	rospy.loginfo("Building network")
	# ANN with  N_SONAR inputs and
	# two outputs for linear and angular velocities
	
	# TODO: Initialize network topology. Use the global variable ann to refer the network
	# The ANN *must* define N_SONAR input neurons and two output neurons

	return ann

def controlLoop(weights):
	global ann
	rospy.loginfo("Weights needed: " + str(len(ann.params)) + ", got " + str(len(weights)))

	if (len(ann.params) != len(weights)): rospy.loginfo("WARN: Bad size")
	ann._setParameters(weights)

	vel = Twist()
	iterations = 0

	rate = rospy.Rate(10)
	while (not rospy.is_shutdown()) and iterations < 20: # 20 iterations seems enoght
		out = ann.activate(ranges)

		vel.linear.x = out[0] * LINEAR_MUL
		vel.angular.z = out[1] * ANGULAR_MUL
		velTopic.publish(vel)
		iterations = iterations + 1
		#rospy.loginfo(iterations)
		rate.sleep()
	# Stop robot motion
	vel.linear.x = 0
	vel.angular.z = 0
	velTopic.publish(vel)

	fit = math.sqrt((math.pow(1-odom[0], 2)+ math.pow(1-odom[1], 2)))
	rospy.loginfo("Fitness: " + str(fit))
	#ann._setParameters([0] * len(ann.params))
	ann = initANN()
	return(fit)

def handle_computeFitness(req):
	# Stop robot motion
	# (Needed because of previous runs)
	vel = Twist()
	vel.linear.x = 0
	vel.angular.z = 0
	velTopic.publish(vel)

	rospy.loginfo("Init neurocontrol")
	weights = []
	for i in req.ann: weights.append(i)
	rospy.loginfo(weights)
	# Reset simulation
	try:
		call(["rosservice", "call", "/robot0/replace", "[1,1,1]"]) # TODO: Fix this 
		fitness = controlLoop(weights)
		#reset = rospy.ServiceProxy("/robot0/replace", Pose2D)
		#pose = Pose2D()
		#pose.x = 10
		#pose.y = 10
		#pose.theta = 0
		#response = reset(pose)
		#print(pose)
	except rospy.ServiceException:
		print "Service call failed"

	return fitness

if __name__ == '__main__':
	rospy.init_node('ga_controller')
	
	# Stop robot motion
	# (Needed because of previous runs)
	velTopic = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size=10)
	vel = Twist()
	vel.linear.x = 0
	vel.angular.z = 0
	velTopic.publish(vel)

	ann = initANN()

	for i in range(N_SONAR):
		rospy.Subscriber("/robot0/sonar_"+str(i), Range, callbackSonar, i)

	rospy.Subscriber("/robot0/odom", Odometry, callbackOdom)

	rospy.Service('computeFitness', computeFitness, handle_computeFitness)
	rospy.loginfo("Waiting")
	rospy.spin()


