# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:32:12 2016

@author: pkg
"""
"""
Implementing Character Segmentation by a generic class
Bansal, V. and Sinha, R. (2001). A complete ocr for printed hindi text in devanagari
script. In Document Analysis and Recognition, 2001. Proceedings. Sixth International
Conference on, pages 800{804. IEEE.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import PIL
from PIL import Image

def rgb2gray(rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
        
class Segment:   

    def __init__(self,image):
        gray = image 
       # gray = rgb2gray(image)  #Uncomment for jpg, comment for jpg
        lobs = gray < gray.mean()  
        self.img = lobs
        self.pix_present = []
        self.length,self.width = lobs.shape
        self.length = int(self.length/3)
        self.line_segments = []
        self.Pen_width = 0
        #print line segments
        line_seg =  self.line_segment()
        for i in range(len(line_seg)):
            plt.imshow(lobs[line_seg[i][0]:line_seg[i][1]])
            plt.show()
            
            
        #print word segments
        for i in range(len(line_seg)):
            word_seg =self. word_segment(line_seg[i][0],line_seg[i][1])
            for j in range(len(word_seg)):
                plt.imshow(lobs[line_seg[i][0]:line_seg[i][1],word_seg[j][0]:word_seg[j][1]])
                plt.show()
                
        
        #print word segments without shirorekha into zones top + corebottom
        
        for i in range(len(line_seg)):
            word_seg = self.word_segment(line_seg[i][0],line_seg[i][1])
            for j in range(len(word_seg)):
                headerl1,headerl2 = self.header_line(line_seg[i][0],line_seg[i][1],word_seg[j][0],word_seg[j][1])
                #remove header
                lobs = self.remove_header_line(line_seg[i][0],line_seg[i][1],word_seg[j][0],word_seg[j][1])
                plt.imshow(lobs[line_seg[i][0]:line_seg[i][1],word_seg[j][0]:word_seg[j][1]])
                plt.show()
                #top zone and its individual characters
                plt.imshow(lobs[line_seg[i][0]:headerl1,word_seg[j][0]:word_seg[j][1]])
                plt.show()
                char_segs = self.character_segments(line_seg[i][0],headerl1,word_seg[j][0],word_seg[j][1])
                for segments in char_segs:
                    plt.imshow(lobs[segments[0]:segments[1],segments[2]:segments[3]])
                    plt.show()
                #find bottom zone
                headerl3 = self.bottom_line(headerl2,line_seg[i][1],word_seg[j][0],word_seg[j][1])
                #middle zone and then its independent characters
                plt.imshow(lobs[headerl2:headerl3,word_seg[j][0]:word_seg[j][1]])
                plt.show()
                headerl3 = int(headerl3  or 0)
                char_segs = self.character_segments(headerl2,headerl3,word_seg[j][0],word_seg[j][1])
                for segments in char_segs:
                    plt.imshow(lobs[segments[0]:segments[1],segments[2]:segments[3]])
                    plt.show()
                #bottom zone and independent characters
                headerl3 = int(headerl3 or 0)
                if headerl3 < line_seg[i][1]:
                    plt.imshow(lobs[headerl3:line_seg[i][1],word_seg[j][0]:word_seg[j][1]])
                    plt.show()
                char_segs = self.character_segments(headerl3,line_seg[i][1],word_seg[j][0],word_seg[j][1])
                for segments in char_segs:
                    plt.imshow(lobs[segments[0]:segments[1],segments[2]:segments[3]])
                    plt.show()
            
    #gives a list of beggining and ending index of each line in whole text
    def line_segment(self):
        for i in range(self.length):
            self.pix_present.append(0)
            for j in range(self.width):
                if self.img[i][j] == True :
                    self.pix_present[i]+=1
        i = 0
        while i < self.length:
            while i < self.length and self.pix_present[i] == 0 :
                i+=1
                
            if i == self.length :
                break
            tmp = i
            while i < self.length and self.pix_present[i] != 0 :
                i+=1

            if i == self.length :
                self.line_segments.append([tmp,i-1])
            else :
                self.line_segments.append([tmp,i])
        return self.line_segments
        
    #gives a list of beggining and ending index of each word in a line 
    def word_segment(self,l1,l2):
        word_segments = []
        line_pix_present = []
        for i in range(self.width):
            line_pix_present.append(0)
            for j in range(l1,l2+1):
                if self.img[j][i] == True :
                    line_pix_present[i]+=1
        i = 0
        while i < self.width:
            while i < self.width and line_pix_present[i] == 0 :
                i+=1
                
            if i == self.width :
                break
            tmp = i
            while i < self.width and line_pix_present[i] != 0 :
                i+=1

            if i == self.width :
                word_segments.append([tmp,i-1])
            else :
                word_segments.append([tmp,i])
        return word_segments
        
    # gives the index range for shirorekha for each word
    def header_line(self,l1,l2,w1,w2):
        line_pix_present = []
        for i in range(l1,l2+1):
            line_pix_present.append(0)
            for j in range(w1,w2+1):
                if self.img[i][j] == True :
                    line_pix_present[-1]+=1
        i = np.array(line_pix_present).argmax() + l1
        j = i
        k = i
        while j > l1 and line_pix_present[j-l1]>=.9*line_pix_present[i-l1]:
            j-=1
        while k < l2 and line_pix_present[k-l1]>=.9*line_pix_present[i-l1]:
            k+=1
        self.Pen_width = k - j
        return [j+1,k-1]
    
    #removes shirorekha
    def remove_header_line(self,l1,l2,w1,w2):
        headerx1,headerx2 = self.header_line(l1,l2,w1,w2)
        self.img[headerx1:headerx2+1,w1:w2] = 0
        return self.img
   
   #To find bottom line for seperating into bottom zone
    def bottom_line(self,l1,l2,w1,w2):
        char_height = []
        pix_count = []
        for i in range(w1,w2+1):
            pix_count.append(0)
            for j in range(l1,l2+1):
                if self.img[j][i] == True :
                    pix_count[i-w1]+=1
        i = w1
        while i < w2:
            while i<w2+1 and pix_count[i-w1] == 0:
                i+=1
            if i == w2 + 1 :
                break
            m = pix_count[i-w1]
            while i<w2+1 and pix_count[i-w1] != 0:
                if pix_count[i-w1] > m:
                    m = pix_count[i-w1]
                i+=1
            char_height.append(m)
        if len(char_height)!=0:
            charHmax = char_height[np.array(char_height).argmax()]
            if len(char_height)==1 :
                return l2 #forsingle character input
            cat1 = cat2 = cat3 = 0
            for i in range(len(char_height)):
                if char_height[i]>0.8*charHmax:
                    cat1+=1
                elif char_height[i]>=0.64*charHmax:
                    cat2+=1
                else:
                    cat3+=1
            if cat1>=cat2 and cat1 >= cat3 :
                tmp = charHmax
            elif cat2>=cat1 and cat2 >= cat3 :
                tmp = 0                
                for i in range(len(char_height)):
                    if char_height[i]>0.64*charHmax and char_height[i]<0.8*charHmax and char_height[i]>tmp:
                        tmp = char_height[i]
            else:
                tmp = 0                
                for i in range(len(char_height)):
                    if char_height[i]<0.64*charHmax and char_height[i]>tmp:
                        tmp = char_height[i]
            if charHmax - tmp >= charHmax/4 :
                return tmp + l1
            return charHmax + l1 - 1
    
    #segment each word into individual character
    def character_segments(self,l1,l2,w1,w2):
        char_segs = []
        pix_count = []
        for i in range(w1,w2+1):
            pix_count.append(0)
            for j in range(l1,l2+1):
                if self.img[j][i] == True :
                    pix_count[i-w1]+=1
        i = w1
        while i < w2:
            while i<w2+1 and pix_count[i-w1] == 0:
                i+=1
            if i == w2 + 1 :
                break
            char_w1 = i
            while i<w2+1 and pix_count[i-w1] != 0:
                i+=1
            char_w2 = i-1
            j = l1
            k = 0
            while j<l2:
                for k in range(char_w1,char_w2):
                   if self.img[j][k] == True :
                       break
                if self.img[j][k] == True :
                    break
                j+=1
            char_l1 = j
            j = l2
            while j>l1:
                for k in range(char_w1,char_w2):
                   if self.img[j][k] == True :
                       break
                if self.img[j][k] == True :
                    break
                j-=1
            char_l2 = j
            if 1.4*(char_l2 - char_l1) > char_w2  - char_w1 :
                char_segs.append([char_l1,char_l2,char_w1,char_w2])
            else:
                C = self.segment_fused_character(char_l1,char_l2,char_w1,char_w2)
                char_segs.append([char_l1,char_l2,char_w1,C])
                char_segs.append([char_l2,char_l2,C,char_w2])
        return char_segs
    
    #Generate collapsed horizontal projection
    def generate_CHP(self,l1,l2,w1,w2):
        CHP = []
        for i in range(l1,l2+1):
            CHP.append(0)
            for j in range(w1,w2+1):
                if self.img[i][j] :
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
        
    #find the vertical line index to segment fused characters
    def segment_fused_character(self, l1, l2, w1, w2):  
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
                if self.img[j][i] :
                    temp = temp + 1
            if temp >= Final_right_pixels:
                Final_right_pixels = temp
                Final_right = i
        
        if Final_right_pixels > (Conj_bottom-Conj_top+1)*.9:# calculate pen width here
            Conj_right = Final_right - self.Pen_width
        
        #plt.imshow(lobs[Conj_top:Conj_bottom+1,Conj_left:Conj_right+1])
        #plt.show()
        
        #2. Initialise  C1
        C1 = Conj_right - self.Pen_width
        
        #3.,4. Computing Discontinuity
        while C1>Conj_left_onethird:
            CHP,R1,R2,R3,CHP_height = self.generate_CHP(Conj_top,Conj_bottom,C1,Conj_right)    
            if R3 == len(CHP) and CHP_height > Conj_height/3 and C1 < Conj_right_onethird:
                break
            else:
                C1-=1
                
        #plt.imshow(lobs[Conj_top:Conj_bottom+1,Conj_left:C1+1])
        #plt.show()
        
        #5. 6. Computing CHP2 and assigning class
        CHP2,R1,R2,R3,CHP2_height = self.generate_CHP(Conj_top,Conj_bottom,Conj_left,Conj_left_onethird)
        if CHP2_height >= .8*Conj_height:
            Class = 2
        else:
            Class = 1
        # 7. class1 for c2
        if Class == 1:
            C2 = Conj_left_onethird + 1
            while C2 < Conj_mid :
                CHP3,R1,R2,R3,self.CHP3_height = self.generate_CHP(Conj_top,Conj_bottom,Conj_left,C2)
                if self.CHP3_height <= .3*Conj_height:
                    C2+=1
                else:
                    break
            if self.CHP3_height <= .3*Conj_height and C2 < Conj_mid :
                while C2 < Conj_mid:
                    black_pix_in_C2 = 0
                    black_pix_in_C2_next = 0
                    for i in range(Conj_top,Conj_bottom+1):
                        black_pix_in_C2+=self.img[i][C2]
                        black_pix_in_C2_next+=self.img[i][C2+1]
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
                    temp+=self.img[j][i]
                if temp>=Black_pixels_count:
                    Black_pixels_count = temp
                    C2 = i
            C2+=1
            while C2 < Conj_mid:
                black_pix_in_C2 = 0
                black_pix_in_C2_next = 0
                for i in range(Conj_top,Conj_bottom+1):
                    black_pix_in_C2+=self.img[i][C2]
                    black_pix_in_C2_next+=self.img[i][C2+1]
                if black_pix_in_C2 <= black_pix_in_C2_next :
                    C2+=1
                else:
                    break
        
        #plt.imshow(lobs[Conj_top:Conj_bottom+1,Conj_left:C2+1])
        #plt.show()
        #compute segment line
        C = int((C1+C2)/2)
        return C
        
        
        
#Calling function        
image = mpimg.imread('./4.jpg') 
Segment(image)
 