'''
This script is used for processing on a batch of videos and
using FFMPEG to do series of jobs

Copyright 2018 chesterw@bu.edu by Zifan Wang
'''

import os
from threading import Thread
import time
from queue import Queue

QUEUE = Queue()
QUEUE_HQ = Queue()

COUNT_HQ = 0
COUNT = 0
TOTAL = 0
TMP = []


def ffmpeg_hq():
    '''
    Convert file to 720p at 2Mbps and 30fps
    '''
    global COUNT_HQ, QUEUE_HQ, TOTAL
    while True:
        if not QUEUE_HQ.empty():
            print("[FFMPEG_HQ]Working on the "+str(COUNT_HQ+1)+" job.")
            single_file = QUEUE_HQ.get()
            os.system("ffmpeg -i "+single_file+" -b 2M -r 30 -f mp4 -s 1280x720 -loglevel quiet "+str(COUNT_HQ)+"_HQ.mp4")
            COUNT_HQ += 1
            print("[FFMPEG_HQ]Finished "+str(COUNT_HQ + COUNT)+" now. "+str(TOTAL - COUNT - COUNT_HQ)+" left.")
            time.sleep(3)


def ffmpeg():
    '''
    Convert file to 480p at 1Mbps and 30fps
    '''
    global COUNT, COUNT_HQ, QUEUE, TOTAL
    while True:
        if not QUEUE.empty():
            print("[FFMPEG]Working on the "+str(COUNT+1)+" job.")
            single_file = QUEUE.get()
            os.system("ffmpeg -i "+single_file+" -b 1M -r 30 -f mp4 -s 640x480 -loglevel quiet "+str(COUNT)+".mp4")
            COUNT += 1
            print("[FFMPEG]Finished "+str(COUNT + COUNT_HQ)+" now. "+str(TOTAL - COUNT - COUNT_HQ)+" left.")
            time.sleep(3)


def inmodule():
    '''
    Get file path from user's input
    '''
    global QUEUE, QUEUE_HQ, TOTAL, TMP
    while True:
        if QUEUE.empty() and QUEUE_HQ.empty() and TOTAL - COUNT - COUNT_HQ == 0:
            filepath = input("[Input]Give file paths, split by space:\n")
            if filepath:
                TMP = filepath.split(" ")
                TOTAL += 2 * len(TMP)
                for item in TMP:
                    QUEUE.put(item)
                    QUEUE_HQ.put(item)


THREADS = []
T1 = Thread(target=ffmpeg_hq)
THREADS.append(T1)
T2 = Thread(target=ffmpeg)
THREADS.append(T2)
T3 = Thread(target=inmodule)
THREADS.append(T3)

for thread in THREADS:
    thread.start()
