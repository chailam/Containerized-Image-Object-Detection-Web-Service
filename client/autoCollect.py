"""
Created by: Chai Lam Loi
13/4/2021
Web service

autoCollect  is a Python script to automatically run the iWebLens_client.py command five times with threads "1", "6", "11", "16","21", "26" and "31".
It will return an array of average response time and that array can be used to plot the 
"Impact of Num of Threads in Client and Num of Pods in Cluster on Response Time of Service". 

Note: the input for the y axis has to be entered manually because the number of pods on the server has to be
scaled manually.

Note: You have to manually scale the pod from 1 to 3. This script could not scale the pod on server.

Run the autoCollect script using:
 "python autoCollect.py <path-to-input-image-folder>".

"""

import subprocess
import matplotlib.pyplot as plt
import re
import time
import sys
import numpy as np


def autoSendCMD (inputfolder):
    threadNo= ["1", "6", "11", "16","21", "26", "31"]
    resultArray = []
    hostIP = "http://118.138.241.47:30000" 
    serverIP = hostIP + "/api/objectdetection"

    try:
        # Run for many thread
        for thread in threadNo:
            time.sleep(5)
            tmp = []
            # Each thread run for multiple times
            for repeat in range(5):
                # Run the command
                print('Running command (repeat: ',repeat,' ):', 'python iWebLens_client.py', inputfolder ,serverIP , thread)
                result = subprocess.run(['python', 'iWebLens_client.py', inputfolder, serverIP, thread], stdout=subprocess.PIPE)
                # Retrieve and decode the result
                resultString = result.stdout.decode('utf-8',errors="ignore")
                averageTime = re.search("average response time: \d*\.\d*",resultString)
                averageTime = re.search("\d*\.\d*",averageTime.group()).group()
                tmp.append(float(averageTime))
            # Calculate the average of average time
            average = sum(tmp)/len(tmp)
            resultArray.append(average)
            print("Average for",thread," : ",average)

        print(resultArray)

    except Exception as e:
        print("Exception in webservice call: {}".format(e))


def drawPlot ():
    threadNo= [1, 6, 11, 16, 21, 26, 31]
    # the pod1, pod2, and pod3 array value have to be inputted manually after performing the 
    # autoSendCMD function above using 1, 2 or 3 pods
    pod1 = [1.4537831246852875, 0.6688168291002512, 0.6861622110009193,0.7068228330463171,0.7632072456181049, 0.8416027650237083, 1.5567676164209843]
    #[1.7201039433479308, 0.656352274864912, 0.6751330923289061, 0.6900314178317786, 0.7395405165851117, 2.0449401825666427, 0.8690988175570965]
    #1.4537831246852875, 0.6688168291002512, 0.6861622110009193,0.7068228330463171,0.7632072456181049, 0.8416027650237083, 1.5567676164209843
    pod2 = [1.4334193859249353, 0.45027200505137444, 0.4428413361310959, 0.3862167187035084, 1.3496532153338194, 2.2015235397964714, 3.9570875708013773]
    # [1.5071401368826627, 0.39816702604293824, 0.37341747134923936, 0.38740396723151205, 1.3496532153338194, 2.2015235397964714, 3.9570875708013773]
    # 1.4334193859249353, 0.45027200505137444, 0.4428413361310959, 0.3862167187035084, 0.4167259633541107, 1.0452121943235397, 5.456946711987257]
    pod3 = [1.420014806091785, 0.3270368233323097, 0.2949784118682146, 0.2830626517534256, 0.3732285462319851, 2.1678637508302927, 3.133410330861807]
    # [1.3725603513419629, 0.3270368233323097, 0.28717867359519006, 0.846693479642272, 2.7601728715002536, 2.915730521082878, 6.6715162999928]
    # [1.5448190510272979, 0.354247385263443, 1.0317521557211875, 1.3098264440894127, 1.0479171983897686, 2.4090786658227445, 2.153183848038316]
    """
    Manually calculate each once (either on the 5124 VM<<< or 5225 VM) and write report
    """
    x = np.arange(1, 32, 5)
    plt.xticks(x)
    plt.plot(threadNo, pod1, label = "1 Pod")
    plt.plot(threadNo, pod2, label = "2 Pod")
    plt.plot(threadNo, pod3, label = "3 Pod")
    plt.xlabel("Number of Threads")
    plt.ylabel("Mean of Average Response Time (s)")
    plt.title("Impact of Num of Threads in Client and Num of Pods in Cluster on Response Time of Service")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    inputfolder = sys.argv[1]
    autoSendCMD(inputfolder)
    drawPlot()

