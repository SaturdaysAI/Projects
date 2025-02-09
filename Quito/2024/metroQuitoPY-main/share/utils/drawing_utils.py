import cv2
import numpy as np

from share.constants.config import (ALERT_COLOR, GREEN_COLOR, ROI_COLOR,
                                    YELLOW_COLOR)

        
def draw_detections(frame, boxes, class_ids, yellow_band_points, classes):
    for i, box in enumerate(boxes):
        x, y, w, h = box

        # Increase box width
        w = int(w * 3)
        x = x - int(w * 0.25)
        x = max(x, 0)

        # Check if the person crosses the yellow stripe using cv2.pointPolygonTest
        if yellow_band_points is not None:
            # Convert yellow_band_points to a NumPy array (if it isn't already)
            yellow_band_polygon = np.array(yellow_band_points, dtype=np.int32)

            # Get the center of the person's box
            person_center = (x + w // 2, y + h // 2)

            # Use cv2.pointPolygonTest to check if the center of the person is inside the polygon
            distance = cv2.pointPolygonTest(yellow_band_polygon, person_center, False)

            # If the point is inside the polygon, the distance will be positive.
            if distance >= 0:
                cv2.putText(frame, "Cruzando la franja amarilla", (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ALERT_COLOR, 2)
                cv2.putText(frame, "ALERTA: Cruzan la linea", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, ALERT_COLOR, 2)

        if yellow_band_points is not None:
            cv2.drawContours(frame, [yellow_band_points], -1, YELLOW_COLOR, 2)
        
        # Draw the boxes with the new width
        color = (GREEN_COLOR)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        
        label = f"{classes[class_ids[i]]}"
        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 0.5, color, 2)