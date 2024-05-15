import pickle

import cv2
import mediapipe as mp
import numpy as np
from Note import Note

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

wave_type = 'sawtooth'
oktawa = 4
labels_dict = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
while True:

    data_aux = []
    x_ = []
    y_ = []
    z_ = []

    ret, frame = cap.read()

    H, W, A = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  
                hand_landmarks,  
                mp_hands.HAND_CONNECTIONS,  
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                z = hand_landmarks.landmark[i].z
                x_.append(x)
                y_.append(y)
                z_.append(z)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                z = hand_landmarks.landmark[i].z
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
                data_aux.append(z - min(z_))
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        z1 = int(min(z_) * A) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10
        z2 = int(max(z_) * A) - 10

        if len(data_aux) != 63:
            if len(data_aux) < 63:
                data_aux += [0] * (63 - len(data_aux))
            elif len(data_aux) > 63:
                cv2.putText(frame, f"SCHOWAJ JEDNA REKE DLA LEPSZYCH WYNIKOW", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 230), 3, cv2.LINE_AA)
                data_aux = data_aux[:63]
                
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]
        nuta = str(predicted_character).lower() + str(oktawa)

        Note(nuta, duration=0.05).play(wave_type=wave_type)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (180, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1.3, (0, 0, 255), 3,
                    cv2.LINE_AA)
        cv2.putText(frame, f"Octave: {oktawa}", (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1.8, (130, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(frame, f"Wave type: {wave_type}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1.8, (80, 0, 0), 3, cv2.LINE_AA)


    cv2.imshow('frame', frame)
    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
        break
    # patches
    elif key == ord('a'):
        wave_type = 'sawtooth'
        oktawa = 4
    elif key == ord('s'):
        wave_type = 'square'
        oktawa = 5
    elif key == ord('d'):
        wave_type = 'sine'
        oktawa = 6
    elif key == ord('f'):
        wave_type = 'triangle'
        oktawa = 6
    # wave type
    elif key == ord('z'):
        wave_type = 'sawtooth'
    elif key == ord('x'):
        wave_type = 'square'
    elif key == ord('c'):
        wave_type = 'sine'
    elif key == ord('v'):
        wave_type = 'triangle'
    # octave
    elif key == ord('0'):
        oktawa = 0
    elif key == ord('1'):
        oktawa = 1
    elif key == ord('2'):
        oktawa = 2
    elif key == ord('3'):
        oktawa = 3
    elif key == ord('4'):
        oktawa = 4
    elif key == ord('5'):
        oktawa = 5
    elif key == ord('6'):
        oktawa = 6
    elif key == ord('7'):
        oktawa = 7
    elif key == ord('8'):
        oktawa = 8

cap.release()
cv2.destroyAllWindows()