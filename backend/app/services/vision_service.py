# Appel du modèle CV, resize d'images
import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO

MODEL_PATH = "/app/data/models/plant_disease_model.keras"
CLASSES_PATH = "/app/data/models/class_names.json"

_vision_model = None
_class_names = None

def load_model_and_classes():
    """Charge le modèle Keras et la liste des classes (Singleton)."""
    global _vision_model, _class_names
    
    if _class_names is None:
        if not os.path.exists(CLASSES_PATH):
            raise FileNotFoundError(f"Fichier de classes introuvable : {CLASSES_PATH}")
        with open(CLASSES_PATH, 'r') as f:
            _class_names = json.load(f)

    if _vision_model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modèle Keras introuvable : {MODEL_PATH}")
        print(" Chargement du modèle de Vision EfficientNet...")
        _vision_model = tf.keras.models.load_model(MODEL_PATH)

def predict_disease_from_image(image_bytes: bytes) -> str:
    """Prend une image en binaire, la formate pour EfficientNet et retourne la maladie."""
    load_model_and_classes()
    
    # 1. Ouvrir l'image avec PIL
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    
    # 2. Redimensionner à la taille attendue par ton modèle (256x256)
    image = image.resize((256, 256))
    
    # 3. Convertir en Array Numpy et ajouter la dimension du batch
    img_array = tf.keras.utils.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0) # Devient (1, 256, 256, 3)

    # 4. Prédiction
    predictions = _vision_model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])
    
    # 5. Trouver le nom de la maladie
    maladie_detectee = _class_names[predicted_class_index]
    print(f"Maladie détectée par la Vision : {maladie_detectee}")
    
    return maladie_detectee