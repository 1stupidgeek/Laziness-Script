# PLEASE MAKE SURE that while running the script, you focus on the tab that is playing the content, if you focus ont he windows that
# displays the camera output, this script wont work.


import cv2
import mediapipe
import webbrowser
import pyautogui
import time

webbrowser.open("www.youtube.com/shorts")

camera = cv2.VideoCapture(0)

w_width = 480
w_height = 640

time.sleep(4) #some-time for the browser to load
pyautogui.click()

mediaPipeHands = mediapipe.solutions.hands
mediaPipeDraw = mediapipe.solutions.drawing_utils
hands = mediaPipeHands.Hands()
window_name = "Lazy Hands"
prev_coords = {}

while True:
    success, frame = camera.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            mediaPipeDraw.draw_landmarks(frame, hand, mediaPipeHands.HAND_CONNECTIONS)
            for id, landmark in enumerate(hand.landmark):

                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cy_index = cy if id == 8 else 0

                if id in prev_coords:                    
                    change = cy_index - prev_coords[id]
                    if change < -70: 
                        pyautogui.press("down")
                prev_coords[id] = cy_index
                
                if id == 8: #index finger
                    cv2.line(frame, (w_height//2, 0), (cx, cy), (255, 0, 255), 10)

    cv2.imshow(window_name, frame)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)


    keyCode = cv2.waitKey(50)
    win_prop = cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE)

    if keyCode != -1:
        break
    if win_prop <= 0:
        break
