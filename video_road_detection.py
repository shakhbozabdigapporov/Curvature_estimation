import cv2
from hybridnets import HybridNets, optimized_model


test = 'challenge_video.mp4'
cap = cv2.VideoCapture(test)
start_time = 0 # skip first {start_time} seconds
cap.set(cv2.CAP_PROP_POS_FRAMES, start_time*30)

# Initialize road detector
# model_path = "models/mhn_regnety_384x640.onnx"
# anchor_path = "models/mhn_regnety_384x640.npy"

model_path = "models/hybridnets_512x640.onnx"
anchor_path = "models/anchors_512x640.npy"

optimized_model(model_path) # Remove unused nodes
roadEstimator = HybridNets(model_path, anchor_path, conf_thres=0.5, iou_thres=0.5)

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (1280,720))

cv2.namedWindow("Road Detections", cv2.WINDOW_NORMAL)	
while cap.isOpened():

	# Press key q to stop
	if cv2.waitKey(1) == ord('q'):
		break

	try:
		# Read frame from the video
		ret, new_frame = cap.read()
		if not ret:	
			break
	except:
		continue
	
	# Update road detector
	seg_map, filtered_boxes, filtered_scores = roadEstimator(new_frame)

	combined_img = roadEstimator.draw_2D(new_frame)

	cv2.imshow("Road Detections", combined_img)
	out.write(combined_img)

out.release()