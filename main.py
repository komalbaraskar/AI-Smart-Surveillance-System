import cv2
import time
from ultralytics import YOLO
from tracker import process_tracks
from heatmap import update_heatmap
from alert import send_alert
from config import CROWD_THRESHOLD
from face_recog import load_faces, recognize_face
from database import save_log, save_count

# Load face data
load_faces()

# YOLO + Camera
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

history = []
sent_alerts = set() 

# Control DB saving frequency
last_saved_time = 0

# Zone drawing
zones = []
drawing = False

def draw_zone(event, x, y, flags, param):
    global drawing, zones

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        zones = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        zones.append((x, y))

cv2.namedWindow("Detection")
cv2.setMouseCallback("Detection", draw_zone)

# MAIN LOOP
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO DETECTION
    results = model(frame)
    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])

            if cls == 0:  # person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, 'person'))

    # TRACKING
    tracks_data = list(process_tracks(detections, frame))

    # FACE RECOGNITION
    faces, names = recognize_face(frame)

    for (top, right, bottom, left), name in zip(faces, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # Save recognized face
        if name != "Unknown":
            save_log(f"{name} detected")

    # DRAW TRACKS + ALERTS
    for track_id, (l, t, r, b), alerts in tracks_data:
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id}", (l, t - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Zone detection
        if len(zones) == 2:
            if zones[0][0] < l < zones[1][0] and zones[0][1] < t < zones[1][1]:
                msg = f"⚠ Zone intrusion ID {track_id}"
                if msg not in sent_alerts:
                    send_alert(msg)
                    save_log(msg)
                    sent_alerts.add(msg)

        # Behavior alerts
        for alert in alerts:
            if alert not in sent_alerts:
                print(alert)
                send_alert(alert)
                save_log(alert)
                sent_alerts.add(alert)

    # CROWD ANALYSIS
    people_count = len(tracks_data)
    history.append(people_count)

    # Save count every 2 seconds
    if time.time() - last_saved_time > 2:
        save_count(people_count)
        last_saved_time = time.time()

    # Overcrowding
    if people_count > CROWD_THRESHOLD:
        if "crowd" not in sent_alerts:
            msg = "⚠ Overcrowding detected"
            send_alert(msg)
            save_log(msg)
            sent_alerts.add("crowd")

    # Trend detection
    if len(history) > 3 and history[-1] > history[-2] > history[-3]:
        if "trend" not in sent_alerts:
            msg = "⚠ Crowd increasing trend"
            send_alert(msg)
            save_log(msg)
            sent_alerts.add("trend")

    # HEATMAP
    boxes = [box for _, box, _ in tracks_data]
    heatmap_img = update_heatmap(boxes)

    # DRAW ZONE
    if len(zones) == 2:
        cv2.rectangle(frame, zones[0], zones[1], (0, 0, 255), 2)

    # DISPLAY
    cv2.imshow("Detection", frame)
    cv2.imshow("Heatmap", heatmap_img)

    # EXIT
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Exiting program...")
        break

# CLEAN EXIT
cap.release()
cv2.destroyAllWindows()