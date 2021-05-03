#!/usr/bin/python3

# check the person is in image
# if so, add a number of person.txt
# if not, just reset the file

import jetson.inference
import jetson.utils
import cv2
import argparse
import sys

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)

# process frames until the user exits
while True:
	img = input.Capture()
	detections = net.Detect(img, overlay=opt.overlay)
	print("detected {:d} objects in image".format(len(detections)))


	# Something detected
	for detection in detections:

		# Patient in
		if detection.ClassID == 1:
			print("Yes There is!")
		
			# Change Number of txt file
			with open("count_10min.txt","rt") as f:
		
				# First time : Write 1 
				if not f.readline():
					with open("count_10min.txt","a") as fa: fa.writelines(["\n","1"])
		
				# Not First : Add Number
				else:
					last = f.readlines()[-1]
					with open("count_10min.txt","a") as fa: fa.writelines(["\n","{}".format(int(last)+1)])
			break

		# No Patient
		else:
			print("No There isnt")
		
			# Reset Number of file
			with open("count_10min.txt","w") as fw: pass
	
	# Nothing detected
	if not detections:
		print("No There isnt")
		
		# Reset Number of txt file
		with open("count_10min.txt","w") as fw: pass
	
	
	
	if not input.IsStreaming() or not output.IsStreaming():
		break


