import cv2
import imutils
from imutils.video import FPS
import numpy
import time

class ResizeFrame:
    def __init__(self, q1=None, q2=None, file1=None):
        self.hudDoneQueue = q1
        self.resizeDoneQueue = q2
        self.stopped = False  # indicates if thread should be stopped
        self.currentFrame = None
        self.file1 = file1 #used for file logging
        self.done = False

    def resize(self):
        #print("DF started")
        while not self.stopped:
            if not self.hudDoneQueue.empty():
                self.currentFrame = self.hudDoneQueue.get()
                self.currentFrame.frame = imutils.resize(self.currentFrame.frame, width=1000)
                self.file1.write("RS1: {:.2f} Got frame {} from hudDoneQueue\n".format((time.time() * 1000), self.currentFrame.name))
            # else:
            # 	#print("DF: {:.2f} hudDoneQueue empty".format(time.time()*1000))
            if not self.resizeDoneQueue.full():
                self.resizeDoneQueue.put(self.currentFrame,
                                      block=True)  # Block is true so it will wait for other thread/process to finish
                self.file1.write("RS2: {:.2f} Put frame {} to resizeDoneQueue (resizeDoneQueue size: {})\n".format((time.time() *
                                                                                                  1000),
                                                                                                 self.currentFrame.name,
                                                                                                 self.resizeDoneQueue.qsize()))
            else:  # resizeDoneQueue is full
                self.resizeDoneQueue.get()  # remove the oldest frame to make room for the new frame
                self.resizeDoneQueue.put(self.currentFrame, block=True)

    def stop(self):
        self.stopped = True