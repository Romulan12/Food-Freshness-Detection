import flask
from flask import Flask, jsonify, request
import requests
import  os
from os.path import dirname, join
import datetime

import json
import logging
import configparser
import time
from detection_model import modelPrediction
from waitress import serve

config = configparser.RawConfigParser()
config.read(os.path.join(os.getcwd() , "../config/config.property"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(thread)d:%(threadName)s:%(process)d:%(message)s")
file_handler = logging.FileHandler('../logs/freshnessDetection.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())

STATUSMESSAGE = dict(config.items("STATUSMESSAGE"))
messageL20037 = STATUSMESSAGE["l20037"]
messageE50063 = STATUSMESSAGE["e50063"]
messageE50064 = STATUSMESSAGE["e50064"]


APIENDPOINT = dict(config.items('APIENDPOINT'))
endpointapi = APIENDPOINT['endpoint']
port_no = APIENDPOINT["port_no"]

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True


class_names = ['F_Banana', 'F_Lemon', 'F_Lulo', 'F_Mango', 'F_Orange', 'F_Strawberry', 'F_Tamarillo', 'F_Tomato', 'S_Banana', 'S_Lemon', 'S_Lulo', 'S_Mango', 'S_Orange', 'S_Strawberry', 'S_Tamarillo', 'S_Tomato']
batch_size = 32
img_height = 180
img_width = 180
num_classes = 16

def generateResponse(imgPath, freshness, outRequest, statuscode, start):

    if freshness[0] == "S":
        food_detection = "STALE"
    elif freshness[0] == "F":
        food_detection = "FRESH"
    else: 
        food_detection = "NA"


    if(outRequest == "NA"):
        if(statuscode == "E50063"):
            return {"imgpath": imgPath, "foodStatus":food_detection, "foodLabel": outRequest, "statusCode": statuscode, "statusMessage": messageE50063, "timeTaken": time.time()-start},500
        elif(statuscode == "E50064"):
            return {"imgpath": imgPath, "foodStatus":food_detection, "foodLabel": outRequest, "statusCode": statuscode, "statusMessage": messageE50064, "timeTaken": time.time()-start},500
        else:
            print("UNHANDLED EXCEPTION")
            return {"imgpath": imgPath, "foodStatus":food_detection, "foodLabel": outRequest, "statusCode": statuscode, "statusMessage": messageE50063, "timeTaken": time.time()-start},500
    else :
        return {"imgpath": imgPath, "foodStatus":food_detection,  "foodLabel": outRequest, "statusCode": statuscode, "statusMessage": messageL20037, "timeTaken": time.time()-start},200
            


@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    start = time.time()
    logger.info("INVALID REQUEST")
    resp, httpCode = generateResponse("NA","NA","NA",'E50010',start)
    return resp, 500


@app.route(endpointapi, methods = ["POST"])
def damage_detection_api():
    start = time.time()
    requestsParam  = request.get_json()
    imgPath = requestsParam["docpath"]
    
    logger.info("IMAGEPATH {}".format(imgPath))
    try:
        out_label, freshness , statuscode = modelPrediction(imgPath, img_height, img_width, num_classes, class_names, logger)
        resp, httpCode = generateResponse(imgPath, freshness , out_label, statuscode, start)

    except:
        logger.exception("CANNOT CONNECT TO SERVER")
        resp, httpCode = generateResponse(imgPath, "NA", "NA", "E50063" , start)
    return resp, httpCode

if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = port_no)
   