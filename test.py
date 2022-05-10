import sys
import os
from tkinter.font import BOLD
from tkinter.tix import Tree
from tokenize import String
import cv2
import numpy as np
import dlib
from math import hypot
import time
import pyglet


#================SOUND===========================#

rightsound = pyglet.media.load("1640627565260-voicemaker.in-speech.mp3",streaming=False)
leftsound = pyglet.media.load("1640627581472-voicemaker.in-speech.mp3",streaming=False)
sound = pyglet.media.load("mixkit-typewriter-soft-click-1125.wav",streaming=False)

#================CV Functions======================#
cap = cv2.VideoCapture(0)




#================DLIB functions====================#
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_SIMPLEX

#===============KEYBOARD===========================#
keyboard = np.zeros((400,500,3),np.uint8)
board = np.zeros((300,300,3),np.uint8)
board[:] = (255,255,255)

key_set_1 = {0 : "1" , 1 : "2" , 2 : "3" , 3 : "4" , 4 : "5" , 5 : "6" , 6 : "7" , 7 : "8" , 8 : "9" , 9 : "0" ,
           10 : "Q" , 11 : "W" , 12 : "E" , 13 : "R" , 14 : "T" , 15 : "Y" , 16 : "U" , 17 : "I" , 18 : "O" , 19 : ">" }

key_set_2 = { 0 : "A" , 1 : "S" , 2 : "D" , 3 : "F" , 4 : "G" , 5 : "H" , 6 : "J" , 7 : "K" , 8 : "L" , 9 : "Z" ,
           10 : "X" , 11 : "C" , 12 : "V" , 13 : "B" , 14 : "N" , 15 : "M" , 16 : "P" , 17 : "+" , 18 : "_" , 19 : ">"}

def letter(x,y,text,light):
  height = 100
  width = 100
  th = 1
  if(light == True):
    cv2.rectangle(keyboard,(x+th,y+th),(x + width - th , y + height - th),(225,225,225),-1)
  else:
    cv2.rectangle(keyboard,(x+th,y+th),(x + width - th , y + height - th),(0,225,0),0)
  font_scale = 2
  font_th = 1
  text_size = cv2.getTextSize(text,font,font_scale,font_th)
  text_width,text_height = text_size[0][0],text_size[0][1]
  text_x = int((width-text_width)/2) + x
  text_y = int((height+text_height)/2) + y
  cv2.putText(keyboard,text,(text_x,text_y),font,font_scale,(0,0,225),font_th)
def draw_keyboard(key_set,idx):
  hei = 0
  light = True
  ii = 0
  for i in range(4):
    wid = 0
    for j in range(5):
      if(idx==ii):
        light = True
      else:
        light = False
      letter(wid,hei,key_set[ii],light)
      ii=ii+1
      wid = wid + 100
    hei = hei + 100
def draw_menu():
  height = 400
  width = 250
  th = 1
  x = 0
  y = 0
  text = "LEFT"
  cv2.rectangle(keyboard,(x+th,y+th),(x + width - th , y + height - th),(0,225,0),0)
  font_scale = 2
  font_th = 1
  text_size = cv2.getTextSize(text,font,font_scale,font_th)
  text_width,text_height = text_size[0][0],text_size[0][1]
  text_x = int((width-text_width)/2) + x
  text_y = int((height+text_height)/2) + y
  cv2.putText(keyboard,text,(text_x,text_y),font,font_scale,(0,0,225),font_th)
  x = 250
  y = 0
  text = "RIGHT"
  cv2.rectangle(keyboard,(x+th,y+th),(x + width - th , y + height - th),(0,225,0),0)
  font_scale = 2
  font_th = 1
  text_size = cv2.getTextSize(text,font,font_scale,font_th)
  text_width,text_height = text_size[0][0],text_size[0][1]
  text_x = int((width-text_width)/2) + x
  text_y = int((height+text_height)/2) + y
  cv2.putText(keyboard,text,(text_x,text_y),font,font_scale,(0,0,225),font_th)


#=================FUNCTIONS=========================#
def eye_ratio(eye_points,facial_landmarks):
  left = (facial_landmarks.part(eye_points[0]).x,facial_landmarks.part(eye_points[0]).y)
  right = (facial_landmarks.part(eye_points[3]).x,facial_landmarks.part(eye_points[3]).y)
  centre_top = ((facial_landmarks.part(eye_points[1]).x+facial_landmarks.part(eye_points[2]).x)//2,(facial_landmarks.part(eye_points[1]).y+facial_landmarks.part(eye_points[2]).y)//2)
  centre_bottom = ((facial_landmarks.part(eye_points[5]).x+facial_landmarks.part(eye_points[4]).x)//2,(facial_landmarks.part(eye_points[5]).y+facial_landmarks.part(eye_points[4]).y)//2)
  # lines eyes 
  # hor_line1 = cv2.line(frame,left,right,(0,225,0),1)
  # ver_line1 = cv2.line(frame,centre_top,centre_bottom,(0,225,0),1)
  horline_eye1 = hypot((left[0]-right[0]),(left[1]-right[1]))
  verline_eye1 = hypot((centre_top[0]-centre_bottom[0]),(centre_top[1]-centre_bottom[1]))
  ratio1 = horline_eye1/verline_eye1
  return ratio1




def LR_ratio(eye_points,landmarks,height,width,name):

  # left eye
  left_eye_region = np.array([(landmarks.part(eye_points[0]).x,landmarks.part(eye_points[0]).y),(landmarks.part(eye_points[1]).x,landmarks.part(eye_points[1]).y),(landmarks.part(eye_points[2]).x,landmarks.part(eye_points[2]).y),(landmarks.part(eye_points[3]).x,landmarks.part(eye_points[3]).y),(landmarks.part(eye_points[4]).x,landmarks.part(eye_points[4]).y),(landmarks.part(eye_points[5]).x,landmarks.part(eye_points[5]).y)],np.int32)
  #cv2.polylines(frame,[left_eye_region],True,(0,255,0),4)
  mask = np.zeros((height,width),np.uint8)
  cv2.polylines(mask,[left_eye_region],True,255,4)
  cv2.fillPoly(mask,[left_eye_region],255)
  left_eye = cv2.bitwise_and(gray,gray,mask=mask)
  min_x = np.min(left_eye_region[:,0])
  max_x = np.max(left_eye_region[:,0])
  min_y = np.min(left_eye_region[:,1])
  max_y = np.max(left_eye_region[:,1])
  eye = left_eye[min_y:max_y,min_x:max_x]
  # gray_eye = cv2.cvtColor(eye,cv2.COLOR_BGR2GRAY)
  _,eye_threshold = cv2.threshold(eye,110,255,cv2.THRESH_BINARY)
  dst = cv2.resize(eye_threshold, None, fx = 5, fy = 5, interpolation = cv2.INTER_CUBIC)
  cv2.imshow(name,dst)
  # cv2.imshow("mask",left_eye)
  # cv2.resize(eye,None,fx=5,fy=5)
  hei,wid = eye_threshold.shape
  left_eye_threshold = eye_threshold[0:hei,0:int(wid/2)]
  left_eye_nonwhite = cv2.countNonZero(left_eye_threshold)
  right_eye_threshold = eye_threshold[0:hei,int(wid/2):wid]
  right_eye_nonwhite = cv2.countNonZero(right_eye_threshold)
  if (left_eye_nonwhite)+(right_eye_nonwhite) == 0:
    return 0
  if right_eye_nonwhite > 0:
    return (left_eye_nonwhite)/(right_eye_nonwhite)
  else:
    return 0


#==================== variables +================#

fram = 0
idx = 0
blinks = 0
contr = 0
alph = 'A'
st = ""
select = True
lastselect = True
lr_menu = True
ci = 1
line = 50
aa = "re"
eae = "red"
#=======================main==========================#


while True:
  _,frame = cap.read()
  frame = cv2.resize(frame, None, fx = 1.5, fy = 1.5, interpolation = cv2.INTER_CUBIC)
  keyboard[:] = (0,0,0)
  fram += 1
  if lr_menu == True :
    draw_menu()
  if select == True:
    key_set = key_set_1
  else :
    key_set = key_set_2
  alph = key_set[idx]
  gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  faces = detector(gray)
  for face in faces:
    # print(face)
    # x,y = face.left(),face.top()
    # x1,y1 = face.right(),face.bottom()
    cv2.rectangle(frame,(face.left(),face.top()),(face.right(),face.bottom()),(0,255,0),4)
    # eye 1

    landmarks = predictor(gray,face)
    for ii in range(0,68):
      cv2.circle(frame, (landmarks.part(ii).x, landmarks.part(ii).y), 1, (0, 0, 255), -1)
    right_eye_region = np.array([(landmarks.part(42).x,landmarks.part(42).y),(landmarks.part(43).x,landmarks.part(43).y),(landmarks.part(44).x,landmarks.part(44).y),(landmarks.part(45).x,landmarks.part(45).y),(landmarks.part(46).x,landmarks.part(46).y),(landmarks.part(47).x,landmarks.part(47).y)],np.int32)
    height,width,_ = frame.shape
    gaz_left = LR_ratio([36,37,38,39,40,41],landmarks,height,width,aa)
    gaz_right = LR_ratio([42,43,44,45,46,47],landmarks,height,width,eae)
    gaz_ratio = (gaz_right+gaz_left)/2
    ratio1 = eye_ratio([36,37,38,39,40,41],landmarks)
    ratio2 = eye_ratio([42,43,44,45,46,47],landmarks)
    final_eye_ratio = (ratio1+ratio2)/2
    # gaze detection
    if lr_menu == True:
      # cv2.putText(frame,str(gaz_left),(50,150),font,2,(0,0,225),3)
      # cv2.putText(frame,str(gaz_right),(50,200),font,2,(0,0,225),3)
      if gaz_ratio <= 0.6 :
        contr+=1
        select = True
        if contr==15:
            lr_menu = False
            contr = 0
            fram =  0
            rightsound.play()
        if select!= lastselect:
          lastselect = select
          contr = 0
      elif gaz_ratio >= 1.4 :
        contr+=1
        select = False
        if contr==15:
            lr_menu = False
            fram =  0
            leftsound.play()
        if select!= lastselect:
          lastselect = select
          contr = 0
      else :
        contr = 0
    else:
      contr = 0
    if lr_menu == False:
      if final_eye_ratio>4.9:
        # cv2.putText(frame , str(blinks) , (10,line), font , 2 , (0,0,255))
        blinks+=1
        fram-=1
        if blinks==5:
          if alph != "+" and alph != "<" and alph != "_" and alph!= ">":
            st += alph
          elif alph == "<":
            stm = st[:-1]
            st = stm
          elif alph == "+":
            line += 50
          elif alph == "_":
            st+=" "
          elif alph == ">" :
            lr_menu = True
          sound.play()
          board[:] = (255,255,255)
      else:
        blinks = 0
    # cv2.resize(eye_threshold,None,fx=5,fy=5)
    # cv2.imshow("eye",eye_threshold)
    # cv2.resize(right_eye_threshold,None,fx=5,fy=5)
    # cv2.imshow("right",right_eye_threshold)
    # cv2.resize(left_eye_threshold,None,fx=5,fy=5)
    # cv2.imshow("left",left_eye_threshold)
    cv2.putText(frame,str(gaz_ratio),(50,100),font,2,(0,0,225),3)
    # cv2.putText(frame,str(right_eye_nonwhite),(350,100),font,2,(0,0,225),3)
    # cv2.imshow("eye2",eye)
    # cv2.imshow("Mask",left_eye)
  if lr_menu == False:  
    if fram==13 :
      idx = idx+1
      fram = 0
      if idx==20:
        idx = 0
    draw_keyboard(key_set,idx)
  cv2.imshow("keyboard",keyboard)
  cv2.imshow("board",board)
  cv2.putText(board,st,(20,100),font,1,(0,0,0),2)
  fra = cv2.resize(frame, None, fx = 0.4, fy = 0.4, interpolation = cv2.INTER_CUBIC)
  cv2.imshow("frame",fra)
  key = cv2.waitKey(1)
  if(key==27):
    break
cap.release()
cv2.destroyAllWindows()