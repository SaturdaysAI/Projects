import torch
from share.constants.config import CONFIDENCE_THRESHOLD
from ultralytics import YOLO

def load_yolo_model(model_path):
    """
    Carga el modelo YOLO desde el path dado.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device", device)
    return YOLO(model_path).to(device)

def perform_yolo_detection(model, frame):
    """
    Realiza la detección de personas con YOLO.
    """
    results = model(frame)
    boxes, class_ids = [], []

    for result in results:
        for box in result.boxes:
            if box.conf[0] > CONFIDENCE_THRESHOLD and int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                boxes.append([x1, y1, x2 - x1, y2 - y1])
                class_ids.append(int(box.cls[0]))

    return boxes, class_ids

def load_classes(classes_file):
    """
    Carga las clases desde el archivo de clases.
    """
    with open(classes_file, "r") as f:
        return f.read().strip().split("\n")