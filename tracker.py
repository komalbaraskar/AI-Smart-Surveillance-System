from deep_sort_realtime.deepsort_tracker import DeepSort
import time
from config import LOITER_TIME

tracker = DeepSort(max_age=30)
entry_time = {}

def process_tracks(detections, frame):
    global entry_time

    tracks = tracker.update_tracks(detections, frame=frame)
    alerts = []

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = map(int, track.to_ltrb())

        # Store entry time
        if track_id not in entry_time:
            entry_time[track_id] = time.time()

        duration = time.time() - entry_time[track_id]

        if duration > LOITER_TIME:
            alerts.append(f"⚠ Loitering detected ID {track_id}")

        yield track_id, (l, t, r, b), alerts