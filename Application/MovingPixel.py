import time, threading
import sys
import board
import neopixel
from typing import Tuple

solidMovingPixelColor = (255, 0, 0, 0)
trailing1MovingPixelColor = (100, 0, 0, 0)
trailing2MovingPixelColor = (32, 0, 0, 0)

solidSteadStatePixelColor = (0, 0, 255, 0)


centerPixelIndex = 0
pixelCount = 50
brightness = 1.0
isForwardDirection = True

def ClearPixels(index: int, isForward: bool):
   pixels.fill(solidSteadStatePixelColor)


def SetPixels(index: int, isForward: bool):
    pixels[index] = solidMovingPixelColor
    
#    if isForward:
#        if (index - 1) >= 0:
#            pixels[index - 1] =  trailing1MovingPixelColor
#        if (index - 2 ) >= 0:
#            pixels[index - 2] =  trailing2MovingPixelColor
#    else:
#        if (index + 1) <= (pixelCount - 1):
#            pixels[index + 1] =  trailing1MovingPixelColor
#        if (index  + 2 ) <= (pixelCount - 1):
#            pixels[index + 2] =  trailing2MovingPixelColor

def UpdatePixelPosition(index: int, isForward: bool) -> Tuple[int, bool]:
    if isForward:
        index += 1
        if index >= pixelCount:
            index = pixelCount - 2
            isForward = not isForward
    else:
        index -= 1
        if index < 0:
            index = 1
            isForward = not isForward
            
    return index, isForward
    
def UpdatePixel():
    global centerPixelIndex
    global pixels
    global isForwardDirection
    
    ClearPixels(centerPixelIndex, isForwardDirection)

    centerPixelIndex, isForwardDirection = UpdatePixelPosition(centerPixelIndex, isForwardDirection)

    SetPixels(centerPixelIndex, isForwardDirection)
    
    #Write the updated pixels to the hardware
    pixels.show()
    

# Main

print("Running Moving Pixel program...")

# auto_write=False means the LEDs won't be updated until .show() is called which can save tons of write cycles
pixels = neopixel.NeoPixel(board.D21, pixelCount, bpp=4, brightness=brightness, auto_write=False)

pixels.fill(solidSteadStatePixelColor)

ticker = threading.Event()

while not ticker.wait(.05):
    UpdatePixel()



# Fills the whole string with the same color
#pixels.fill((255, 0, 0, 255));

# Sets the first pixel to white
#pixels[0] = (0, 255, 0, 0)