import sys
import os
import cv2
import numpy as np
import dlib
import pyglet
from math import hypot

font = cv2.FONT_HERSHEY_SIMPLEX

keyboard = np.zeros((600,1000,3),np.uint8)

key_set = { 0 : "Q", 1 : "W", 2 : "E", 3 : "R", 4 : "T",
            5 : "A", 6 : "S", 7 : "D", 8 : "F", 9 : "G",
            10 : "Z", 11 : "X", 12 : "C", 13 : "V", 14 : "B",}

def letter(x,y,text,light):
  height = 200
  width = 200
  th = 3
  if(light == True):
    cv2.rectangle(keyboard,(x+th,y+th),(x + width - th , y + height - th),(225,225,225),-1)
  else:
    cv2.rectangle(keyboard,(x+th,y+th),(x + width - th , y + height - th),(0,225,0),th)
  font_scale = 5
  font_th = 4
  text_size = cv2.getTextSize(text,font,font_scale,font_th)
  text_width,text_height = text_size[0][0],text_size[0][1]
  text_x = int((width-text_width)/2) + x
  text_y = int((height+text_height)/2) + y
  cv2.putText(keyboard,text,(text_x,text_y),font,font_scale,(0,0,225),font_th)

def draw_keyboard(key_set):
  hei = 0
  ii = 0
  for i in range(3):
    wid = 0
    for j in range(5):
      letter(wid,hei,key_set[ii],True)
      ii=ii+1
      wid = wid + 200
    hei = hei + 200

draw_keyboard(key_set)

cv2.imshow("keyboard",keyboard)
cv2.waitKey(0)
cv2.destroyAllWindows()