import cv2, time, pandas
from datetime import datetime

video=cv2.VideoCapture(0)
first_frame = None
frame_count = 0
start       = time.time()
status_list = [None,None]
times       = []
df          = pandas.DataFrame(columns=["Start", "End"])
while True:
   frame_count = frame_count + 1
   check, frame = video.read()
   status = 0

   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   gray = cv2.GaussianBlur(gray, (21,21), 0)
   
   if first_frame is None:
      first_frame = gray
      continue
      
   delta_frame  = cv2.absdiff(first_frame, gray)
   thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
   thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
   (_,cnts,_)   = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   for contour in cnts:
      if cv2.contourArea(contour) < 12000: #change this number depending on the distance of the
         continue      
      
      status = 1
      (x,y,w,h) = cv2.boundingRect(contour)
      cv2.rectangle(frame, (x, y), (x+w,y+h), (0,255,0), 3)
      
   status_list.append(status)
   if status_list[-1] == 1 and status_list[-2] == 0:
      times.append(datetime.now())
   elif status_list[-1] == 0 and status_list[-2] == 1:
      times.append(datetime.now())
   
   cv2.imshow("Gray Frame", gray)
   cv2.imshow("Delta Frame", delta_frame)
   cv2.imshow("Threshold", thresh_frame)
   cv2.imshow("Color Frame", frame)
   
   key=cv2.waitKey(1)
   
   if key==ord('q'):
      if status == 1:
         times.append(datetime.now())
      break
      
elapsed=time.time() - start
for i in range(0, len(times), 2):
   df = df.append({"Start" : times[i], "End" : times[i+1]}, ignore_index=True)
   
df.to_csv("movement_detected.csv")
   
print("Running time:" + str(elapsed))
print("Average FPS: " + str(frame_count/elapsed))


video.release()
cv2.destroyAllWindows()