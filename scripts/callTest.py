#!/usr/bin/env python

import rospy

from geometry_msgs.msg import *

from subprocess import call

#rospy.init_node("simulationServer")

#try:
	#pose = Pose2D()
	#pose.x = 10
	#pose.y = 10
	#pose.theta = 0
	#reset = rospy.ServiceProxy("/robot0/replace", pose)
	#response = reset(pose)
arg = "".join(str(range(18))).replace(" ", "")
res = call(["rosservice", "call", "/computeFitness", arg])
print(res)
#except rospy.ServiceException:
#	print "Service call failed"


#rospy.spin()
#
