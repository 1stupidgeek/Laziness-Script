# PLEASE MAKE SURE that while running the script, you focus on the tab that is playing the content, if you focus ont he windows that
# displays the camera output, this script wont work.

import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import time

# Use this if you want to open a browser other than your default browser ->
# put your browser.exe path here
# browser_path = (r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")

#put your browser name instead of brave in here -
# webbrowser.register("brave", None, webbrowser.BackgroundBrowser(browser_path))
# webbrowser.get("brave").open("https://www.youtube.com/shorts")

# Use this if you are happy with your default browser ->
webbrowser.open("www.youtube.com/shorts")

time.sleep(4) #some time for the browser to load
pyautogui.click()

window_name = "Face Scroller"
video = cv2.VideoCapture(0)
mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5)

w_width = 480
w_height = 640

prev_coords = {}

while True:
    success, frame = video.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:
            
            mp_draw.draw_landmarks(frame, face, mp_face_mesh.FACEMESH_TESSELATION)
            for id, landmark in enumerate(face.landmark):

                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cy_index = cy if id == 152 else 0 #targeting the landmark on the chin

                if id in prev_coords:
                    change = cy_index - prev_coords[id]
                    if(change < -13):
                        print(change)
                        pyautogui.press("down")
                prev_coords[id] = cy_index

                if id == 152:
                    cv2.line(frame, (w//2, 0), (cx, cy), (255, 0, 255), 10)
    cv2.imshow(window_name, frame)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    keyCode = cv2.waitKey(50)
    win_prop = cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE)

    if keyCode != -1:
        break
    if win_prop <= 0:
        break
