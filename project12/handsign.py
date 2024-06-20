import time
import HandTrackingModule as hd
import pyautogui 
import numpy as np 
import urllib.request
# import autopy
import cv2

mobile_cap = 'http://192.0.0.4:8080/video'
cap = cv2.VideoCapture(0)
pyautogui.FAILSAFE = False

cam_wid,cam_hig = 600,800
frameW,frameH = 100,400
frameR = 100
cap.set(3,cam_wid)
cap.set(4,cam_hig)
cap.set(cv2.CAP_PROP_FPS,10)
scr_wid,scr_hig = pyautogui.size()
center_x, center_y = cam_wid //2, cam_hig // 2
print(scr_wid,scr_hig)

smoothed_x_previous, smoothed_y_previous = 0,0

detector = hd.handDetector()



# # Get the FPS of the input video
# fps = cap.get(cv2.CAP_PROP_FPS)

# # Define output video file and its FPS (double the input FPS)
# output_file = 'output.mp4'
# output_fps = fps * 2

# # Define the codec and create a VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(output_file, fourcc, output_fps, 
#                       (int(cap.get(3)), int(cap.get(4))))


# open screen
if cap.isOpened(): print("Success ") 
ptime = 0
while True:

     suc,img = cap.read()
     img = detector.findHands(img)
     lmlist = detector.findPosition(img,False)
    # # mark index finger
     figup = detector.getFingers(img)
     if figup[1] == 1 :
         # cv2.rectangle(img,(frameR,frameR),(cam_wid-frameW,cam_hig-frameH ),(255,55,44),2)
         if len(lmlist) != 0:
            x,y = lmlist[8][1],lmlist[8][2]
            cv2.circle(img,(x,y),10, (255, 0, 0),cv2.FILLED)

            # mouse curser
            x2 = np.interp(x,(frameW,cam_wid-frameW),(0,scr_wid))
            y2 = np.interp(y,(0,cam_hig-frameH),(0,scr_hig))

            # Smoothing (averaging) the cursor position
            smooth_factor = 0.7
            smoothed_x = smooth_factor * x2 + (1 - smooth_factor) * smoothed_x_previous
            smoothed_y = smooth_factor * y2 + (1 - smooth_factor) * smoothed_y_previous

            # Moving the mouse cursor
            pyautogui.moveTo(int(scr_wid - smoothed_x), int(smoothed_y))

            smoothed_x_previous, smoothed_y_previous = smoothed_x, smoothed_y


     if figup[1] == 1 and figup[2] == 1 :
          if len(lmlist) != 0:
            # circle
            x,y = lmlist[8][1],lmlist[8][2]
            x1,y1 = lmlist[12][1],lmlist[12][2]
            cv2.circle(img,(x,y),10, (255, 255, 255),cv2.FILLED)
            cv2.circle(img,(x1,y1),10, (255, 255, 255),cv2.FILLED)

            length , img, infoline = detector.findDistance(8,12,img)
            if length <40:
                cv2.circle(img,(infoline[4],infoline[5]),10, (255, 0, 0),cv2.FILLED)
                pyautogui.click(scr_wid-x2,y2)





   # #   print(figup)   
   #   time.sleep(0.03) 
     
   #  # frame rate
     ctime = time.time()
     fps = 1 / (ctime - ptime)
     ptime = ctime
   #   fps = cap.get(cv2.CAP_PROP_FPS)
    # print fps
     cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    #  print(cap.get(cv2.CAP_PROP_FPS))

     if not suc:
        print("error")
        break
   #   out.write(img)
     cv2.imshow("imge:",img) 
     if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cap.release()
# cv2.destroyAllWindows()

    