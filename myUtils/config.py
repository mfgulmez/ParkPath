""" Optional features config. """

Prototxt = "mobilenet_ssd\MobileNetSSD_deploy.prototxt"   # path to Caffe 'deploy' prototxt file
Model = "mobilenet_ssd\MobileNetSSD_deploy.caffemodel"    # path to Caffe pre-trained model
inputSource = 'Camera'	# camera or video file
LiveCamera = 0      # camera ID
InputFile = ''      # select path video file
OutputFile = ''		# path to optional output visdeo file
Confidence = 0.6	# minimum probability to filter weak detections
SkipFrames = 30		# of skip frames between detections
Log = True          # Auto run/Schedule the software to run at your desired time
