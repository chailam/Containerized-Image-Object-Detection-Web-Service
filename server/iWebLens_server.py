"""
Created by: Chai Lam Loi (28136179)
9/4/2021
Web service
Aim: It is a Python script to receive the POST request from client and leverage the object_detection.py to detect object. 
It then return the JSON output to the client. 
"""

from flask import Flask, request, make_response
import json
import base64
import object_detection 

app = Flask(__name__)


@app.route('/api/objectdetection', methods=['POST'])
def serverMain():
    """
    return: response = the JSON format of required response 
    Aim: This is the main function of server which utilised the object detection service in object_detection.py.
    It received the POST request from client, process the JSON data, parse it to the object detection service,
    receive the output from object detection service, and then send the output back to client in JSON format.
    """

    yolo_path = "yolo_tiny_configs/"

    # Retrieve the posted JSON from iWebLens_client
    data = request.get_json()
    data = json.loads(data)

    image_id = data["id"]
    encoded_image_file = data["image"]

    # Convert the image_file back from base64 encoded string to bytes
    image_file = base64.b64decode(encoded_image_file)

    # Parse the image file to object detection service located in object_detection.py
    output = object_detection.objectDetect(image_file, yolo_path)
    print(output)

    # Construct the json file with image id and output of object detection
    # Ensure at least one detection exists
    if len(output) > 0:
        result = {}
        result['id'] = image_id
        tmp = {}
        temp = []
        for detectedObject in output:
            tmp['label'] = detectedObject[0]
            tmp['accuracy'] = detectedObject[1]
            tmp['rectangle'] = {'height':detectedObject[5], 'left':detectedObject[2],'top':detectedObject[3],'width':detectedObject[4]}
            temp.append(tmp)
            tmp = {}
        result['objects'] = temp

        # Send response back to client
        response = make_response(json.dumps(result, indent=4),200) #status 200 = OK
        response.headers["Content-Type"] = "application/json"
        return response

    # Resutn nothing if no object detected
    response = make_response("NO", 200)
    return response


# since we are using flask Run, we no need app.run
#if __name__ == "__main__":
#   app.run(host='0.0.0.0',port=5000,debug=True) 
    #host='0.0.0.0'to handle remote requests, which tells your operating system to listen on all public IPs


