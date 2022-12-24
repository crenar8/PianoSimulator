import time

import mediapipe as mp
import cv2
import musicalbeeps



# Initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the music notes player
player = musicalbeeps.Player(volume = 0.3, mute_output = False)

while True:
    # Read each frame from the webcam
    _, frame = cap.read()

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark with mediapipe classification & regression
    result = hands.process(framergb)

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:


            for lm in handslms.landmark:
                lmx = int(lm.x * width)
                lmy = int(lm.y * height)
                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            if len(landmarks) == 21 and landmarks[8][1] >= 720:
                noteToPlay = "pause"
                indexOfNoteToPlay = landmarks[8][0] * 7 / width
                if 0 <= indexOfNoteToPlay < 1:
                    noteToPlay = "C"
                elif 1 <= indexOfNoteToPlay < 2:
                    noteToPlay = "D"
                elif 2 <= indexOfNoteToPlay < 3:
                    noteToPlay = "E"
                elif 3 <= indexOfNoteToPlay < 4:
                    noteToPlay = "F"
                elif 4 <= indexOfNoteToPlay < 5:
                    noteToPlay = "G"
                elif 5 <= indexOfNoteToPlay < 6:
                    noteToPlay = "A"
                elif indexOfNoteToPlay >= 6:
                    noteToPlay = "B"
                cv2.putText(frame, noteToPlay, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
                player.play_note(noteToPlay, 0.5)
                time.sleep(0.5)

            print("Posizione indice:"+str(landmarks[8])+" / Altezza Schermo: "+str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))


    widthSegment = int(width / 7)


    doStartWidth = 0
    # print 7 music notes segment in the bottom of the frame
    cv2.putText(frame, "DO", (doStartWidth, height), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    reStartWidth = widthSegment
    cv2.putText(frame, "RE", (reStartWidth, height), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    miStartWidth = widthSegment * 2
    cv2.putText(frame, "MI", (miStartWidth, height), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    faStartWidth = widthSegment * 3
    cv2.putText(frame, "FA", (faStartWidth, height), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    solStartWidth = widthSegment * 4
    cv2.putText(frame, "SOL", (solStartWidth, height), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    laStartWidth = widthSegment * 5
    cv2.putText(frame, "LA", (laStartWidth, height), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    siStartWidth = widthSegment * 6
    cv2.putText(frame, "SI", (siStartWidth, height), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Music Notes", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
