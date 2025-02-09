
import cv2
import numpy as np

from share.constants.config import MOVEMENT_THRESHOLD

def create_dynamic_color_range(selected_points):
    # Convertir la lista de colores a un array de numpy
    colors = np.array(selected_points)
    
    # Promediar los colores seleccionados
    average_color = np.mean(colors, axis=0)
    
    # Usar el color promedio para crear un rango dinámico
    lower_yellow = np.clip(average_color - np.array([10, 50, 50]), 0, 255).astype(np.uint8)
    upper_yellow = np.clip(average_color + np.array([10, 50, 50]), 0, 255).astype(np.uint8)
    
    return lower_yellow, upper_yellow

def detect_yellow_band(frame, selected_points):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow, upper_yellow = create_dynamic_color_range(selected_points)
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 20))
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
    yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=2)
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    yellow_band = None
    if yellow_contours:
        largest_yellow_contour = max(yellow_contours, key=cv2.contourArea)
        yellow_band = cv2.convexHull(largest_yellow_contour)
        
    return yellow_band


def check_train_movement_in_polygon(frame, polygon, prev_frame, threshold):
    """
    Verifica si hay movimiento dentro del área definida por un polígono.

    Args:
        frame (np.ndarray): Frame actual del video.
        polygon (list): Lista de puntos [(x1, y1), (x2, y2), ...] que define el polígono.
        prev_frame (np.ndarray): Frame anterior del video.
        threshold (float): Umbral de movimiento para detectar cambios significativos.

    Returns:
        bool: True si se detecta movimiento dentro del polígono, False en caso contrario.
    """
    print("check_train_movement_in_polygon", polygon)

    # Crear una máscara para el polígono
    mask = np.zeros_like(frame[:, :, 0], dtype=np.uint8)  # Crear máscara monocromática
    polygon_points = np.array(polygon, np.int32)
    cv2.fillPoly(mask, [polygon_points], 255)

    # Convertir los frames a escala de grises
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Calcular la diferencia entre el frame actual y el anterior
    diff = cv2.absdiff(gray_prev_frame, gray_frame)

    # Aplicar la máscara al área del polígono
    masked_diff = cv2.bitwise_and(diff, diff, mask=mask)

    # Calcular el promedio de intensidad en el área del polígono
    movement = np.sum(masked_diff) / np.sum(mask)

    # Detectar si el movimiento supera el umbral
    movement_detected = movement > threshold

    return movement_detected


def select_roi():
    image = cv2.imread('./data/example01.jpg')

    # Select the region of interest manually
    roi = cv2.selectROI("Select ROI", image, fromCenter=False, showCrosshair=True)

    # Display the image with the ROI selected
    x, y, w, h = roi
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("ROI Selected", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"ROI Coordinates: (x1={x}, y1={y}, x2={x + w}, y2={y + h})")


def detect_movement_in_roi(prev_frame, curr_frame, roi_coords, threshold=MOVEMENT_THRESHOLD):
    PIXEL_MAX_VALUE = 255
    x1, y1, x2, y2 = roi_coords

    # Verifica que los frames no sean None
    if prev_frame is None or curr_frame is None:
        raise ValueError("Los frames no pueden ser None.")
    
    # Verifica las dimensiones del ROI
    height, width = prev_frame.shape[:2]
    if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
        raise ValueError(f"Coordenadas ROI fuera de los límites: {roi_coords}")

    # Extrae la región de interés (ROI) de ambos frames
    prev_roi = prev_frame[y1:y2, x1:x2]
    curr_roi = curr_frame[y1:y2, x1:x2]

    # Calcula la diferencia absoluta
    diff = cv2.absdiff(prev_roi, curr_roi)
    
    # Aplica un umbral para filtrar cambios significativos
    _, diff_thresh = cv2.threshold(diff, 30, PIXEL_MAX_VALUE, cv2.THRESH_BINARY)

    # Verifica si el resultado del umbral es válido
    if diff_thresh is None:
        raise ValueError("cv2.threshold devolvió None. Verifique los valores de entrada.")

    # Cuenta los píxeles que representan movimiento en el ROI
    movement_pixels = np.sum(diff_thresh) / PIXEL_MAX_VALUE

    # Detecta si hay suficiente movimiento según el umbral
    return movement_pixels > threshold
