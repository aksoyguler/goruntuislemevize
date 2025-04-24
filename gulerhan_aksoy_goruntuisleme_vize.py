from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import screen_brightness_control as sbc

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)

def koordinat_getir(landmarks, indeks, h, w):
    landmark = landmarks[indeks]
    return int(landmark.x * w), int(landmark.y * h)

def draw_landmarks_on_image(rgb_image, detection_result):
    el_landmark_listesi = detection_result.hand_landmarks
    el_tarafi_listesi = detection_result.handedness
    gorsellestirilmis_goruntu = np.copy(rgb_image)
    h, w, _ = gorsellestirilmis_goruntu.shape

    # Sadece ilk el uzerinde islem yap
    if len(el_landmark_listesi) > 0:
        el_landmarks = el_landmark_listesi[0]
        parmaklar = []

        for nokta1, nokta2 in [(8,6), (12,10), (16,14), (20,18)]:
            x1, y1 = koordinat_getir(el_landmarks, nokta1, h, w)
            x2, y2 = koordinat_getir(el_landmarks, nokta2, h, w)
            parmaklar.append(1 if y1 > y2 else 0)

        x4, y4 = koordinat_getir(el_landmarks, 4, h, w)
        x2, y2 = koordinat_getir(el_landmarks, 2, h, w)
        parmaklar.append(1 if x4 < x2 else 0)

        toplam = 5 - sum(parmaklar)
        gorsellestirilmis_goruntu = cv2.putText(gorsellestirilmis_goruntu, str(toplam), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 4)

        ix, iy = koordinat_getir(el_landmarks, 8, h, w)
        tx, ty = koordinat_getir(el_landmarks, 4, h, w)

        gorsellestirilmis_goruntu = cv2.line(gorsellestirilmis_goruntu, (ix, iy), (tx, ty), (0, 255, 255), 3)

        mesafe = int(np.hypot(tx - ix, ty - iy))
        parlaklik = np.clip(int((mesafe - 20) * (100 / 180)), 0, 100)
        try:
            sbc.set_brightness(parlaklik)
        except Exception as e:
            print("Parlaklik ayarlanamadi:", e)

        gorsellestirilmis_goruntu = cv2.putText(gorsellestirilmis_goruntu, f"Parlaklik: {parlaklik}%", (30, 60),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        el_proto = landmark_pb2.NormalizedLandmarkList()
        el_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=l.x, y=l.y, z=l.z) for l in el_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            gorsellestirilmis_goruntu,
            el_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style()
        )

        x_konumlar = [l.x for l in el_landmarks]
        y_konumlar = [l.y for l in el_landmarks]
        yazi_x = int(min(x_konumlar) * w)
        yazi_y = int(min(y_konumlar) * h) - MARGIN
        el_tarafi = el_tarafi_listesi[0]
        cv2.putText(gorsellestirilmis_goruntu, f"{el_tarafi[0].category_name}",
                    (yazi_x, yazi_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    return gorsellestirilmis_goruntu

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

temel_ayarlar = python.BaseOptions(model_asset_path='hand_landmarker.task')
secenekler = vision.HandLandmarkerOptions(base_options=temel_ayarlar, num_hands=1)
algilayici = vision.HandLandmarker.create_from_options(secenekler)

kamera = cv2.VideoCapture(0)
while kamera.isOpened():
    basarili, goruntu = kamera.read()
    if basarili:
        goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
        mp_goruntu = mp.Image(image_format=mp.ImageFormat.SRGB, data=goruntu)
        tespit_sonucu = algilayici.detect(mp_goruntu)
        gorsel = draw_landmarks_on_image(mp_goruntu.numpy_view(), tespit_sonucu)
        cv2.imshow("Goruntu", cv2.cvtColor(gorsel, cv2.COLOR_RGB2BGR))
        tus = cv2.waitKey(1)
        if tus == ord('q') or tus == ord('Q'):
            break
