# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 01:08:59 2017

@author: pkg
"""

import matplotlib.image as mpimg
import fusedcharsep


img = mpimg.imread('fused_word6.png') 
fusedcharsep.segment_fused_character(img)

img = mpimg.imread('fused_word5.png') 
fusedcharsep.segment_fused_character(img)

img = mpimg.imread('fused_word4.png') 
fusedcharsep.segment_fused_character(img)