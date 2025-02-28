import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep, time
import numpy as np
import cvzone
from pynput.keyboard import Controller

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set Width
cap.set(4, 720)   # Set Height

# Initialize Hand Detector (Supports Two Hands)
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Define Keyboard Layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["SPACE", "", "BACKSPACE"]  
]

# Initialize Virtual Keyboard Controller
keyboard = Controller()

# Initialize Final Text Output
finalText = ""
last_key_pressed = None
last_press_time = 0

# Button Class
class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.text = text
        self.size = size
        self.color = (100, 100, 100)

# Function to Draw Keys
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), button.color, cv2.FILLED)
        
        font_scale = 2 if button.text in ["SPACE", "BACKSPACE"] else 3
        text_x_offset = 60 if button.text == "BACKSPACE" else 40 if button.text == "SPACE" else 25

        cv2.putText(img, button.text, (x + text_x_offset, y + 55),
                    cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), 4)
    return img

# Generate Button List
buttonList = []
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        if key == "SPACE":
            button_size = (350, 85)
        elif key == "BACKSPACE":
            button_size = (250, 85)
        elif key == "":
            continue  
        else:
            button_size = (85, 85)

        buttonList.append(Button([120 * j + 50, 120 * i + 50], key, button_size))  # Increased spacing

# Main Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  

    # Detect Hands
    hands, img = detector.findHands(img)

    # Draw Virtual Keyboard
    img = drawAll(img, buttonList)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]  
            if lmList:
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size

                    # Check if Finger is Over the Key
                    if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (100, 200, 100), cv2.FILLED)  
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        # Ensure Hand Landmarks Exist
                        if len(lmList) > 12:
                            l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
                            print(f"Distance: {l}")

                            if l < 30 and (button.text != last_key_pressed or time() - last_press_time > 1):
                                button.color = (50, 200, 50)  
                                last_key_pressed = button.text
                                last_press_time = time()

                                if button.text == "SPACE":
                                    finalText += " "  
                                    keyboard.press(" ")

                                elif button.text == "BACKSPACE":
                                    finalText = finalText[:-1]  
                                    keyboard.press("\b")  

                                else:
                                    finalText += button.text  
                                    keyboard.press(button.text.lower())  

                                sleep(0.7)  
                            else:
                                button.color = (100, 100, 100)  

    # Display Typed Text
    cv2.rectangle(img, (50, 550), (1200, 620), (50, 50, 150), cv2.FILLED)  
    cv2.putText(img, finalText, (60, 600),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Display Image
    cv2.imshow("AI Virtual Keyboard", img)

    # Press 'q' to Exit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release Resources
cap.release()
cv2.destroyAllWindows()
