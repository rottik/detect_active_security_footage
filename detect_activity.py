

import numpy as np
import cv2
import time
import os
import shutil


def detect_empty_video(video):
    capture = cv2.VideoCapture(video)
    firstFrame = None
    detected=True
    cnt=0
    cnt_move=0
    while True:
        
        (grabbed, frame) = capture.read()
        if not grabbed:
            break
     
        frame = frame[0:-1,0:550]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
     
        if firstFrame is None:
            firstFrame = gray
            continue
            
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
     
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
     
        for c in cnts:
            if cv2.contourArea(c) < 500:
                continue
     
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cnt_move=cnt_move+1
            detected=False
        cnt=cnt+1
        if(cnt==4):
            firstFrame = gray
            cnt=0
        cv2.imshow("Security Feed", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
     
        if key == ord("q"):
            break
    capture.release()
    if(cnt_move<5): return True
    return detected


if(__name__=="__main__"):
    #yesterday=str(int(time.strftime("%Y%m%d"))-1)
    days=[]
    for f in os.listdir("."):
        if(os.path.isdir(f)and (f.startswith('.')==False)):
            days.append(f)
    for day in days:
        yesterday=day
        hours=os.listdir(yesterday)
        if("event" in hours):
            hours.remove("event")
        if("empty" in hours):
            hours.remove("empty")
        hours.sort()

        for hour in hours:
            minutes=os.listdir(yesterday+"/"+hour)
            minutes.sort()
            for minute in minutes:
                typ="event"
                if(detect_empty_video(yesterday+"/"+hour+"/"+minute)):
                    typ="empty"
                if(os.path.isdir(yesterday+"/"+typ+"/"+hour+"/")==False):
                    os.makedirs(yesterday+"/"+typ+"/"+hour)
                print(typ+" "+yesterday+"/"+hour+"/"+minute)
                shutil.move(yesterday+"/"+hour+"/"+minute,yesterday+"/"+typ+"/"+hour+"/"+minute)
        
