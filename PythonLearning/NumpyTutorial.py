# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:26:13 2020

Following this tutorial: https://youtu.be/GB9ByFAIAH4

@author: Sam
"""
import numpy as np

a = np.array([1,2,3])
b = np.array([[9.0, 8.0, 7.0], [6.0, 5.0, 4.0]])
a_dim = a.ndim

#get shape
b_shape = b.shape

#accessing/changing specific elements
#get a specific element [row, column]
#can use -ve indexing too
a_item = a[1,5]

#get a specific element row
a[0, :]

#get a specific column
a[:, 2]

#getting a little more fancy [startindex:endindex:stepsize]
a[0, 1:-1:2]

#3D example
d = np.array([[[1,2],[3,4]], [[5,6], [7,8]]])

#get specific element (work outside in)
#[set, row, column]
d[0, 1, 2]

#initialising different arrays
np.zeros((2,3))
np.ones((4,1,2), dtype='int32')
#specify shape, then number
np.full((2,2), 99)

#splicing arrays
output = np.ones((5,5))
z = np.zeros((3,3))

output[1:4,1:4] = z

#BE CAREFUL WHEN COPYING ARRAYS
a = np.array([1,2,3])
b = a
b[0] = 100
#this also changes a!!!
#use this instead
b = a.copy

before = np.array([[1,2,3,4],[5,6,7,8]])
