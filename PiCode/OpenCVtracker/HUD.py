#add symlink to virtualenv's site-packages dir

from threading import Thread
import cv2
import imutils
import numpy
#will I need numpy?
import queue as Q

class Hud:
	def __init__(self, q=None):
		self.q = q
		self.stopped = False #indicates if thread should be stopped
		
	def start(self, cnts):
		t = Thread(target=self.draw, args=(cnts))
		t.daemon = True
		t.start()
		return self
		
	def draw(self, cnts=(0,)):
		while not self.stopped:
			
			if not (self.q.empty):
				currentFrame = self.q.get()
				try:
					# only proceed if at least one contour was found
					if len(cnts) > 0:
						# find the largest contour in the mask, then use
						# it to compute the minimum enclosing circle and
						# centroid
						trackingStatus = 1
						c = max(cnts, key=cv2.contourArea)
						((x, y), radius) = cv2.minEnclosingCircle(c)
						M = cv2.moments(c)
						center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
						

						# only proceed if the radius meets a minimum size
						if radius > 10:
							# draw the circle and centroid on the frame,
							# then update the list of tracked points
							# then print x/y offset from center and FPS -Jesse Moody
							cv2.circle(currentFrame.frame, (int(x), int(y)), int(radius),
								(0, 255, 255), 2)
							cv2.circle(currentFrame.frame, center, 5, (0, 0, 255), -1)
							
							Xoffset = float((x-(resWidth/2))/(resWidth/2)) #float representing distance from screen center to face center
							Yoffset = float(((resLength/2)-int(y))/(resLength/2))
							
							cv2.putText(currentFrame.frame, currentFPSstr, (30,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
							#cv2.putText(frame, averageFPSstr, (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 2)
							print("hud ready for ", currentFrame.name)
							currentFrame.hudReady = True
				except:
					pass
				if cv2.waitKey(1) == ord("q"):
					self.stopped = True

	def stop(self):
		self.stopped = True
