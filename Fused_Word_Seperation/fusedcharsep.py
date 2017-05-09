# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 12:28:38 2017

@author: pkg
"""
"""
Implemented the algorithm for fused character seperation as stated in
Bansal, V. and Sinha, R. (2002). Segmentation of touching and fused devanagari
characters. Pattern recognition, 35(4):875-893.

"""
Pen_width = 7 # header width + 1
import numpy as np
    
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import PIL
from PIL import Image


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])   
#Real Work Starts Now
def generate_CHP(lobs,l1,l2,w1,w2):
    CHP = []
    for i in range(l1,l2+1):
        CHP.append(0)
        for j in range(w1,w2+1):
            if lobs[i][j] :
                CHP[-1]+=1
                break
    i = 0
    while(i<len(CHP) and CHP[i]==0):
        i+=1
    R1 = i
    while(i<len(CHP) and CHP[i]==1):
        i+=1
    R2 = i
    while(i<len(CHP) and CHP[i]==0):
        i+=1
    R3 = i
    CHP_height = R2-R1
    return CHP,R1,R2,R3,CHP_height
def segment_fused_character(img):  
    gray = rgb2gray(img)    
    gray = img[:,:,3]#comment it for bengali
    #plt.imshow(gray, cmap = plt.get_cmap('gray'))
    #plt.show()
    
    lobs = gray > gray.mean()
    lobs = lobs.astype(int)
    #plt.imshow(lobs)
    #plt.show()
    l,w = lobs.shape
    lobs[17:22,] = 0
    
    
    h = 0
    i = 0
    while h == 0 and i<l:
        for j in range(w):
            if lobs[i][j] == 1:
                h = 1
                break
        if j == w-1:
            i = i+1
            
    l1 = i
    h = 0
    i = l-1
    
    while h == 0 and i>=0:
        for j in range(w):
            if lobs[i][j] == 1:
                h = 1
                break
        if j == w-1:
            i = i-1
    l2 = i
    
    #plt.imshow(lobs[l1:l2+1,])
    #plt.show()
    
    h = 0
    i = 0
    while h == 0 and i<w:
        for j in range(l):
            if lobs[j][i] == 1:
                h = 1
                break
        if j == l-1:
            i = i+1
            
    w1 = i
    h = 0
    i = w-1
    
    while h == 0 and i>=0:
        for j in range(l):
            if lobs[j][i] == 1:
                h = 1
                break
        if j == l-1:
            i = i-1
    w2 = i


      
    plt.imshow(lobs)
    plt.show()    
    #0. Initialise variables
    Conj_top = l1
    Conj_bottom = l2
    Conj_left = w1
    Conj_right = w2
    Conj_left_onethird = int(Conj_left + (Conj_right - Conj_left)/3)
    Conj_right_onethird = int(Conj_left + 2*(Conj_right - Conj_left)/3)
    Conj_mid = int(Conj_left + (Conj_right - Conj_left)/2)
    Conj_height = Conj_bottom - Conj_top
    
    #print(Conj_top,Conj_bottom,Conj_left,Conj_right,Conj_left_onethird,Conj_mid,Conj_height)
    
    
    #1. Find the rightmost final boundary
    Final_right = 0
    Final_right_pixels = 0
    
    for i in range(Conj_left,Conj_right+1):
        temp = 0
        for j in range(Conj_top,Conj_bottom+1):
            if lobs[j][i] :
                temp = temp + 1
        if temp >= Final_right_pixels:
            Final_right_pixels = temp
            Final_right = i
    
    if Final_right_pixels > (Conj_bottom-Conj_top+1)*.9:# calculate pen width here
        Conj_right = Final_right - Pen_width
    
    #plt.imshow(lobs[Conj_top:Conj_bottom+1,Conj_left:Conj_right+1])
    #plt.show()
    
    #2. Initialise  C1
    C1 = Conj_right - Pen_width
    
    #3.,4. Computing Discontinuity
    while C1>Conj_left_onethird:
        CHP,R1,R2,R3,CHP_height = generate_CHP(lobs,Conj_top,Conj_bottom,C1,Conj_right)    
        if R3 == len(CHP) and CHP_height > Conj_height/3 and C1 < Conj_right_onethird:
            break
        else:
            C1-=1
            
    #plt.imshow(lobs[Conj_top:Conj_bottom+1,Conj_left:C1+1])
    #plt.show()
    
    #5. 6. Computing CHP2 and assigning class
    CHP2,R1,R2,R3,CHP2_height = generate_CHP(lobs,Conj_top,Conj_bottom,Conj_left,Conj_left_onethird)
    if CHP2_height >= .8*Conj_height:
        Class = 2
    else:
        Class = 1
    # 7. class1 for c2
    if Class == 1:
        C2 = Conj_left_onethird + 1
        while C2 < Conj_mid :
            CHP3,R1,R2,R3,CHP3_height = generate_CHP(lobs,Conj_top,Conj_bottom,Conj_left,C2)
            if CHP3_height <= .3*Conj_height:
                C2+=1
            else:
                break
        if CHP3_height <= .3*Conj_height and C2 < Conj_mid :
            while C2 < Conj_mid:
                black_pix_in_C2 = 0
                black_pix_in_C2_next = 0
                for i in range(Conj_top,Conj_bottom+1):
                    black_pix_in_C2+=lobs[i][C2]
                    black_pix_in_C2_next+=lobs[i][C2+1]
                if black_pix_in_C2 <= black_pix_in_C2_next :
                    C2+=1  
                else:
                    break
        
    # 8. class2 for c2
    else :
        C2 = 0
        Black_pixels_count = 0
        for i in range(Conj_left,Conj_left_onethird+1):
            temp = 0        
            for j in range(Conj_top,Conj_bottom+1):
                temp+=lobs[j][i]
            if temp>=Black_pixels_count:
                Black_pixels_count = temp
                C2 = i
        C2+=1
        while C2 < Conj_mid:
            black_pix_in_C2 = 0
            black_pix_in_C2_next = 0
            for i in range(Conj_top,Conj_bottom+1):
                black_pix_in_C2+=lobs[i][C2]
                black_pix_in_C2_next+=lobs[i][C2+1]
            if black_pix_in_C2 <= black_pix_in_C2_next :
                C2+=1
            else:
                break
    
    #plt.imshow(lobs[Conj_top:Conj_bottom+1,Conj_left:C2+1])
    #plt.show()
    #compute segment line
    C = int((C1+C2)/2)
    plt.imshow(lobs[Conj_top:Conj_bottom+1,Conj_left:C+1])
    plt.show()
    plt.imshow(lobs[Conj_top:Conj_bottom+1,C+1:w2])
    plt.show()



















































































