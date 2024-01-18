
"""
Modified by: Chai Lam Loi 
9/4/2021
Web service
Aim: It is a Python script to perform object detection using tiny yolo weights and neural net.

Run with following:
"python object_detection.py  yolo_tiny_configs/  <input image>"
"""

# import the necessary packages
import numpy as np
import sys
import time
import cv2
import os

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1

def get_labels(labels_path,yolo_path):
    # load the COCO class labels our YOLO model was trained on
    lpath=os.path.sep.join([yolo_path, labels_path])

    print(yolo_path)
    LABELS = open(lpath).read().strip().split("\n")
    return LABELS


def get_weights(weights_path,yolo_path):
    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weights_path])
    return weightsPath


def get_config(config_path,yolo_path):
    configPath = os.path.sep.join([yolo_path, config_path])
    return configPath


def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def do_prediction(image,net,LABELS):
    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    #print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # the output
    # ensure at least one detection exists

    output = []

    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            output.append([LABELS[classIDs[i]],confidences[i],boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])
            print("detected item:{}, accuracy:{}, X:{}, Y:{}, width:{}, height:{}".format(LABELS[classIDs[i]],
                                                                                             confidences[i],
                                                                                             boxes[i][0],
                                                                                             boxes[i][1],
                                                                                             boxes[i][2],
                                                                                             boxes[i][3]))
    return output


# this console script is made into webservice using Flask.
# The webservice has been created in iWebLens_server.py
def objectDetect(image_file, yolo_Path):
    """
    arg: image_file = the image file in bytes format
        yolo_path = the path to the yolo_tiny_configs folder
    return: output = a list of object detection arrays. Each array has 
            the label, accuracy, x, y, width and height of detected object.
    Aim: the function is constructed to be utlised in iWebLens_server.py, which is the main server file.
    """
    yolo_path  = yolo_Path

    ## Yolov3-tiny version
    labelsPath= "coco.names"
    cfgpath= "yolov3-tiny.cfg"
    wpath= "yolov3-tiny.weights"

    Lables = get_labels(labelsPath, yolo_path)
    CFG = get_config(cfgpath, yolo_path)
    Weights = get_weights(wpath, yolo_path)

    try:
        # since the image has been converted from JSON string to bytes,
        # it has to be converted from bytes to np array to be processed in opencv
        image_as_np = np.frombuffer(image_file, dtype=np.uint8)
        img = cv2.imdecode(image_as_np, flags=1)
        image=img.copy()
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        # load the neural net.  Should be local to this method as its multi-threaded endpoint
        nets = load_model(CFG, Weights)
        output = do_prediction(image, nets, Lables)

    except Exception as e:
        print("Exception  {}".format(e))

    return output



if __name__ == '__main__':
    ## argument
    if len(sys.argv) != 3:
        raise ValueError("Argument list is wrong. Please use the following format:  {} {} {}".
                     format("python iWebLens_server.py", "<yolo_config_folder>", "<Image file path>"))

    imagefile = str(sys.argv[2])
    yolo_path  = str(sys.argv[1])

    objectDetect(imagefile, yolo_path)


