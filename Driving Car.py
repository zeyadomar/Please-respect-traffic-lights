#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np


# In[2]:


import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


   


# In[4]:


vid=cv2.VideoCapture(0)


def search_for_color(img):
    i=0
    j=0
   #note : room lighting affects the threshold values below 
    red=False
    count=0
    for i in range(len(img)):
        count=0
        for j in range(len(img[i])):
            
            if img[i][j]>220 :
                count+=1

            j+=1
        if count>len(img[i])/3:
            red=True
            break

        i+=1
    return red
    
color=[255,255,255]
while True:
    try:
        ret,frame = vid.read()
        
        
        is_red=search_for_color(frame[240:340,300:400,2])
       
        if is_red:
            color=[0,255,0]
        else:
            color=[255,255,255]
        
        cv2.rectangle(frame,(280,300),(340,400),color,3)
       
        
        if   is_red:
            PressKey(0x11)
        else:
            ReleaseKey(0x11)
            
        cv2.imshow("test",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    except:
        pass
        
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 


# In[ ]:





# In[ ]:




