import cv2
import time
import torch
from ultralytics import YOLO

# Cargar el modelo YOLOv8 preentrenado (versión más ligera)
model = YOLO('yolov8n.pt')

# Verificar si se puede usar la GPU con CUDA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Definir una línea para contar los vehículos
line_y = 300  # Y-coordinate of the line

def detect_and_count_vehicles(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Obtener la tasa de fotogramas del video
    count = 0
    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Reducir la resolución del frame para acelerar el procesamiento
        frame = cv2.resize(frame, (640, 480))

        results = model(frame)
        detections = results[0].boxes.data.cpu().numpy()  # Obtener detecciones
        
        for detection in detections:
            x1, y1, x2, y2, conf, cls = detection
            cls = int(cls)
            if cls in [2, 3, 5, 7]:  # Clase de vehículos (coche, motocicleta, bus, camión)
                center_y = (y1 + y2) / 2

                # Verificar si el vehículo cruza la línea
                if line_y - 2 < center_y < line_y + 2:
                    count += 1
                    # Marcar el cruce
                    cv2.line(frame, (int(x1), int(center_y)), (int(x2), int(center_y)), (0, 255, 0), 2)

                # Dibujar la detección
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

        # Dibujar la línea
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 0, 255), 2)

        # Calcular el tiempo transcurrido en segundos en el video
        elapsed_time_seconds = frame_count / fps

        # Calcular el tiempo real transcurrido
        real_time_elapsed = time.time() - start_time

        # Mostrar el contador en la esquina superior izquierda
        cv2.putText(frame, f'Numero de vehiculos: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Mostrar los FPS y el tiempo transcurrido
        #cv2.putText(frame, f'FPS del video: {fps:.2f}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        #cv2.putText(frame, f'Tiempo del video: {elapsed_time_seconds:.2f}s', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        #cv2.putText(frame, f'Tiempo real: {real_time_elapsed:.2f}s', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Mostrar el frame
        cv2.imshow('Vehicle Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

        # Resetear el contador cada minuto
        if elapsed_time_seconds > 60:
            print(f'Numero de vehiculos en el último minuto: {count}')
            count = 0
            frame_count = 0
            start_time = time.time()  # Reiniciar el tiempo real

    cap.release()
    cv2.destroyAllWindows()

# Ruta del video
video_path = r'C:\Users\ezxt99454\Desktop\crisa\Personal\SaturdaysAI\clases\proyecto_final\src\yolo\yolov8\data\autopista1.mp4'
detect_and_count_vehicles(video_path)
