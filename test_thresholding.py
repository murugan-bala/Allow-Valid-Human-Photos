import cv2
import face_recognition
import glob
import os
import logging
import time
import re
import csv
import json
import sys
import flask 
import datetime
import requests
import base64
import logging
import numpy as np
import pandas as pd
import face_recognition
from flask import Flask, send_file
from flask import request
from flask import jsonify
#from waitress import serve
from flask_cors import CORS
from PIL import Image, ImageDraw
#from ocrr import tesseract
#from text_tesseract import tess
app = Flask(__name__)
CORS(app)

#app_name=sys.argv[1]
#date=sys.argv[2]
#print(app_name,date)
try:
    #pass
    #imdir = 'D:\\SIFY\\SIBI\\Photos_signature_validation\\photos\\*.*'
    #imdir = 'D:\\SIFY\\SIBI\\Photos_signature_validation\\incorrect_photos\\*.*'
    #imdir = './photos_sign_100/photos_100/*.*'

    #path = 'D:\\SIFY\\SIBI\\Photos_signature_validation\\struct_photo_sign\\photos\\'+app_name+'\\uploads\\'+date+'\\photo\\'
    path='D:\\SIFY\\SIBI\\pream\\IGIDR\\igidramfeb20_photo&sign\\igidramfeb20\\photos\\'
    if os.path.exists(path):
        print ("Path exist")
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger()
    #logger.addHandler(logging.FileHandler('D:\\SIFY\\SIBI\\Photos_signature_validation\\struct_photo_sign\\photos\\'+app_name+'\\uploads\\'+date+'\\photos_logg.log', 'w'))
    #logger.addHandler(logging.FileHandler('D:\\SIFY\\SIBI\\Photos_signature_validation\\photos_logg.log', 'w'))
    logger.addHandler(logging.FileHandler('igidramfeb20_photos_adaptive_log.log', 'w'))
    printt = logger.info


    # field names  
    fields = ['TimeStamp','ImageName','Results']
     
    # name of csv file  
    filename = "temp_photos.csv"
    count=0
    in_valid=0
    start_time = time.time()
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile,dialect="excel")
        csvwriter.writerow(fields)
        for file in glob.glob(path+'*.*'):
            print(file)
            file_name=file.split('\\')
            unknown_image = face_recognition.load_image_file(file)
            face_locations = face_recognition.face_locations(unknown_image) #face_locations = face_recognition.face_locations(image,model="cnn")
            print("There are ",len(face_locations),"people in this image")
            img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)   # my_photo, incorrect_3
            ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
            n_white_pix = np.sum(thresh1 == 255)
            #print("Binary image shape is :",thresh1.shape)
            print("Total pixels is (Binary image ) :",thresh1.size)
            print('Number of white pixels:', n_white_pix)
            dif=thresh1.size-n_white_pix
            print("different is ",dif)
            print()
            if dif<1000 or n_white_pix>50000:
                now = time.strftime('%d-%m-%Y %H:%M:%S')
                print("Photo is not valid..")
                printt('{}  : In_Valid face detected : {}'.format(now,file))
                in_valid=in_valid+1
                csvwriter.writerows([[now, file_name[-1],"Not valid photo"]])
            else:
                if len(face_locations)==0:
                    now = time.strftime('%d-%m-%Y %H:%M:%S')
                    print("No Faces Detected..")
                    printt('{}  : No face detected : {}'.format(now,file))
                    csvwriter.writerows([[now, file_name[-1],"No face Detected"]])
                elif len(face_locations)>1:
                    now = time.strftime('%d-%m-%Y %H:%M:%S')
                    print("More than One Face detected....")
                    printt('{}  : More then one face detected : {}'.format(now,file))
                    csvwriter.writerows([[now, file_name[-1],"More faces"]])
                #print("Valid photo..")
            count=count+1
            print("*********************counting photos*************** :",count)
    df = pd.read_csv('temp_photos.csv')
    df.dropna(axis=0, how='all',inplace=True)
    df.to_csv('igidramfeb20_latest_log.csv', index=False)
    os.remove("temp_photos.csv")
    print()
    print("total images in the folder is : ",count)
    print("total invalid images in the folder is : ",in_valid)
    print()
    print("---Total time taken  %s seconds ---" % (time.time() - start_time))

except FileNotFoundError:
    print("Please enter valid path .. Folder does not exist.!!!!")
            

