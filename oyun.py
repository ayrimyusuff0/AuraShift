import cv2
import mediapipe as mp
import time
import socket 
#import mediapipe as mp


UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mp_hands = mp.solutions.hands
mp_cizim = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,        
    max_num_hands=1,               
    model_complexity=1,             
    min_detection_confidence=0.75,  
    min_tracking_confidence=0.75    
)

kamera = cv2.VideoCapture(0)
kamera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

pencere_adi = "AuraShift - Vision OS (1080p)"
cv2.namedWindow(pencere_adi, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(pencere_adi, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

onceki_zaman = 0
eski_x, eski_y = 0.5, 0.5 
yumusatma_hizi = 0.12 

print("AuraShift 1080p + Unity Bağlantısı Devrede... [Matrix Modu Aktif]")

while True:
    basarili, kare = kamera.read()
    if not basarili:
        break
        
    kare = cv2.flip(kare, 1)
    h, w, c = kare.shape 

    suanki_zaman = time.time()
    fps = 1 / (suanki_zaman - onceki_zaman) if (suanki_zaman - onceki_zaman) > 0 else 0
    onceki_zaman = suanki_zaman

    rgb_kare = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
    sonuclar = hands.process(rgb_kare)

    if sonuclar.multi_hand_landmarks:
        for el_isaretleri in sonuclar.multi_hand_landmarks:
            lm = el_isaretleri.landmark
            isaret_parmagi_ucu = lm[8]
            bas_parmak_ucu = lm[4]
            bilek = lm[0]
            
            mesafe = ((isaret_parmagi_ucu.x - bas_parmak_ucu.x)**2 + (isaret_parmagi_ucu.y - bas_parmak_ucu.y)**2)**0.5
            
            kapali_parmak_sayisi = 0
            dort_parmak = [(8, 5), (12, 9), (16, 13), (20, 17)]
            
            for uc, kok in dort_parmak:
                mesafe_uc = ((lm[uc].x - bilek.x)**2 + (lm[uc].y - bilek.y)**2)**0.5
                mesafe_kok = ((lm[kok].x - bilek.x)**2 + (lm[kok].y - bilek.y)**2)**0.5
                
                if mesafe_uc < mesafe_kok:
                    kapali_parmak_sayisi += 1

            bas_uc_mesafe = ((lm[4].x - lm[17].x)**2 + (lm[4].y - lm[17].y)**2)**0.5
            bas_kok_mesafe = ((lm[2].x - lm[17].x)**2 + (lm[2].y - lm[17].y)**2)**0.5
            
            if bas_uc_mesafe < bas_kok_mesafe:
                kapali_parmak_sayisi += 1

            yumruk_mu = (kapali_parmak_sayisi == 5)

            if yumruk_mu:
                hareket_durumu = 2 
                daire_renk = (255, 0, 0) 
            elif mesafe < 0.05:
                hareket_durumu = 1 
                daire_renk = (0, 0, 255) 
            else:
                hareket_durumu = 0 
                daire_renk = (255, 255, 255) 

            fark_x = abs(isaret_parmagi_ucu.x - eski_x)
            fark_y = abs(isaret_parmagi_ucu.y - eski_y)
            
            if fark_x > 0.005 or fark_y > 0.005:
                cx_send = eski_x + (isaret_parmagi_ucu.x - eski_x) * yumusatma_hizi
                cy_send = eski_y + (isaret_parmagi_ucu.y - eski_y) * yumusatma_hizi
            else:
                cx_send, cy_send = eski_x, eski_y
                
            eski_x, eski_y = cx_send, cy_send

            data = f"{cx_send},{1-cy_send},{hareket_durumu}" 
            sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))
            
            target_px_x = int(cx_send * w)
            target_px_y = int(cy_send * h)
            
            mp_cizim.draw_landmarks(kare, el_isaretleri, mp_hands.HAND_CONNECTIONS, 
                                    mp_cizim.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1),
                                    mp_cizim.DrawingSpec(color=(0, 255, 255), thickness=1))
            
            cv2.circle(kare, (target_px_x, target_px_y), 8, daire_renk, cv2.FILLED) 
            cv2.circle(kare, (target_px_x, target_px_y), 12, (255, 255, 255), 1)       

    cv2.putText(kare, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(kare, "AURASHIFT V1.2 (CONNECT MODE)", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    
    status_text = "DURUM: BAGLANTI AKTIF" if sonuclar.multi_hand_landmarks else "DURUM: HEDEF ARANIYOR..."
    cv2.putText(kare, status_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow(pencere_adi, kare)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()