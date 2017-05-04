# CS4475 Final Project
# Wing Yi Cheung

import numpy as np
import scipy as sp
import cv2
import scipy.signal
import math

# Sketchify a photo
def getGrayScale(images):
    grayScaleImg = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("A1_Grey_Scale.jpg", grayScaleImg)
    return grayScaleImg

def getNegative(grayScaleImg):
    negativeImg = 255 - grayScaleImg
    cv2.imwrite("A2_Negative.jpg", negativeImg)
    return negativeImg

def getSketchMask(negativeImg, kSize):
    sketchMask = cv2.GaussianBlur(negativeImg, ksize = (kSize, kSize), sigmaX = 0, sigmaY = 0)
    cv2.imwrite("A3_Sketch_Mask.jpg", sketchMask)
    return sketchMask

def Sketchify(grayScaleImg, sketchMask, darkness):
  grayScaleImg = np.uint8(grayScaleImg)
  sketchMask = np.uint8(sketchMask)
  sketch = np.zeros((grayScaleImg.shape[0], grayScaleImg.shape[1]), np.uint8)

  for x in range(grayScaleImg.shape[0]):
    for y in range(grayScaleImg.shape[1]):
      if sketchMask[x,y] == 255:
        sketch[x,y] = 255
      else:
        if grayScaleImg[x,y] * darkness / (255 - sketchMask[x,y]) > 255:
            sketch[x,y] = 255

  sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
  return sketch

# Cartoonize a photo
def SmoothImages(images, smoothScale, blurriness):
    scaledDownImg = np.zeros((images.shape[0], images.shape[1]), np.uint8)
    for i in range(2):
        scaledDownImg = cv2.pyrDown(images)
    for i in range(smoothScale):
        scaledDownImg = cv2.bilateralFilter(scaledDownImg, d = 9,
            sigmaColor = blurriness, sigmaSpace = blurriness)
    for i in range(2):
        smoothedImg = cv2.pyrUp(scaledDownImg)
    cv2.imwrite("B1_Smooth_The_Image.jpg", smoothedImg)
    return smoothedImg

def GetEdgeMask(smoothedImg):
    grayScale = cv2.cvtColor(smoothedImg, cv2.COLOR_RGB2GRAY)
    edgeMask = cv2.adaptiveThreshold(grayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, blockSize = 3, C = 2)
    edgeMask = np.uint8(edgeMask)
    cv2.imwrite("B2_Get_The_Edge.jpg", edgeMask)
    return edgeMask

def EdgesDilation(edgeMask, edgeThickness):
    edgeMask = np.invert(edgeMask)
    dilationKernel = np.ones((edgeThickness, edgeThickness), np.uint8)
    edgeDilation = cv2.dilate(edgeMask, dilationKernel, iterations = 1)
    edgeDilation = np.invert(edgeDilation)
    cv2.imwrite("B3_Thicken_The_Edge.jpg", edgeDilation)
    return edgeDilation

def Toonify(smoothedImg, dilatedEdge):
    dilatedEdge = cv2.cvtColor(dilatedEdge, cv2.COLOR_GRAY2RGB)
    ToonifiedImg = cv2.bitwise_and(dilatedEdge, smoothedImg)
    return ToonifiedImg

def SketchifyVideo (image_list):
    sketchVideo = []
    for i in range(len(image_list)):
        grayscale = getGrayScale(image_list[i])
        neg = getNegative(grayscale)
        mask = getSketchMask(neg, 11)
        sketch = Sketchify(grayscale, mask, 259)
        sketchVideo.append(sketch)
    return sketchVideo

def ToonifyVideo (image_list):
    toonifyVideo = []
    for i in range(len(image_list)):
        SmoothImg = SmoothImages(image_list[i], 7, 15) #blurriness
        edgeMask = GetEdgeMask(SmoothImg)
        DilatedEdges = EdgesDilation(edgeMask, 4) #thickness
        toon = Toonify(smoothedImg, dilatedEdge)
        toonifyVideo.append(toon)
    return toonifyVideo
