import time, threading
import sys
import board
import neopixel
from typing import Tuple

redColor = (255, 0, 0)
greenColor = (0, 255, 0)
blueColor = (0, 0, 255)

orangeColor = (255, 25, 0)
purpleColor = (128, 0, 64)
yellowColor = (255, 100, 0)

whiteColor = (255, 255, 255)
offColor = (0, 0, 0)

solidMovingPixelColor = offColor
solidSteadStatePixelColor = offColor


centerPixelIndex = 0
#pixelCount = 321 # First story LED strip length
pixelCount = 413 # Second story LED strip length
brightness = 1.0
isForwardDirection = True

def ClearPixels(index: int, isForward: bool):
   pixels.fill(solidSteadStatePixelColor)


def SetPixels(index: int, isForward: bool):
    pixels[index] = solidMovingPixelColor
    

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
# Use either board.D18 or board.D21
pixels = neopixel.NeoPixel(board.D21, pixelCount, bpp=3, brightness=brightness, auto_write=False)

pixels.fill(solidSteadStatePixelColor)

ticker = threading.Event()

while not ticker.wait(.017):
    UpdatePixel()



# Fills the whole string with the same color
#pixels.fill((255, 0, 0, 255));

# Sets the first pixel to white
#pixels[0] = (0, 255, 0, 0)
