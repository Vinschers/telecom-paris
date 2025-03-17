#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 22 May 2019

@author: M Roux
"""

import numpy as np
import matplotlib.pyplot as plt

from skimage import io

from skimage import filters


##############################################

import mrlab as mr

##############################################"

############## le close('all') de Matlab
plt.close('all')
################################"


ima = io.imread('pyra-gauss.tif')
sigma = 0
seuilnorme = 0.2

# Gaussian filter
gfima = filters.gaussian(ima, sigma)

# Gradient calculation
gradx = mr.sobelGradX(gfima)
grady = mr.sobelGradY(gfima)

# Gradient magnitude and direction
norme = np.sqrt(gradx ** 2 + grady ** 2)
direction = np.arctan2(grady, gradx)

# Thresholding gradient norm
contoursnorme = (norme > seuilnorme)

# Maxima in gradient direction
contours = np.uint8(mr.maximaDirectionGradient(gradx, grady, 0.2))
valcontours = (norme > seuilnorme) * contours

fig, axs = plt.subplots(3, 3, figsize=(15, 15))

# Displaying all images in subplots
axs[0, 0].imshow(ima, cmap='gray')
axs[0, 0].set_title('Image originale')
axs[0, 0].axis('off')

axs[0, 1].imshow(gfima, cmap='gray')
axs[0, 1].set_title('Image filtrée (passe-bas)')
axs[0, 1].axis('off')

axs[0, 2].imshow(gradx, cmap='gray')
axs[0, 2].set_title('Gradient horizontal')
axs[0, 2].axis('off')

axs[1, 0].imshow(grady, cmap='gray')
axs[1, 0].set_title('Gradient vertical')
axs[1, 0].axis('off')

axs[1, 1].imshow(norme, cmap='gray')
axs[1, 1].set_title('Norme du gradient')
axs[1, 1].axis('off')

axs[1, 2].imshow(direction, cmap='gray')
axs[1, 2].set_title('Direction du Gradient')
axs[1, 2].axis('off')

axs[2, 0].imshow(255 * contoursnorme, cmap='gray')
axs[2, 0].set_title('Norme seuillée')
axs[2, 0].axis('off')

axs[2, 1].imshow(255 * contours, cmap='gray')
axs[2, 1].set_title('Maxima du gradient dans la direction')
axs[2, 1].axis('off')

axs[2, 2].imshow(255 * valcontours, cmap='gray')
axs[2, 2].set_title('Contours filtrés par norme')
axs[2, 2].axis('off')

# Adjust layout for spacing
plt.tight_layout()
plt.show()
