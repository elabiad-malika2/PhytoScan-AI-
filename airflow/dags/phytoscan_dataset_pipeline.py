import os
import re
import random
import shutil
from datetime import datetime, timedelta
from PIL import Image

from airflow import DAG
from airflow.operators.python import PythonOperator


BASE_DIR = "/app/data" 
RAW_DATASET = os.path.join(BASE_DIR, "Plant_leave_diseases_dataset")
RESIZED_DATASET = os.path.join(BASE_DIR, "resized_dataset")
BALANCED_DATASET = os.path.join(BASE_DIR, "balanced_dataset")
FINAL_SPLIT_DATASET = os.path.join(BASE_DIR, "plant_images")



def clean_class_name(name):
    """Nettoie les noms de dossiers (ex: 'Apple___healthy' -> 'apple_healthy')."""
    name = name.lower().replace("___", "_")
    name = re.sub(r"[ ,()\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

def task_resize_and_clean():
    print(" Démarrage du Redimensionnement et Nettoyage...")
    os.makedirs(RESIZED_DATASET, exist_ok=True)

    for cls in os.listdir(RAW_DATASET):
        clean_cls = clean_class_name(cls)
        cls_path = os.path.join(RAW_DATASET, cls)
        new_cls_path = os.path.join(RESIZED_DATASET, clean_cls)
        os.makedirs(new_cls_path, exist_ok=True)

        for img_name in os.listdir(cls_path):
            try:
                img_path = os.path.join(cls_path, img_name)
                img = Image.open(img_path).convert("RGB")
                img = img.resize((256, 256))
                img.save(os.path.join(new_cls_path, img_name))
            except Exception as e:
                print(f"Erreur image ignorée : {img_name}")
                
    print(" Redimensionnement terminé.")


def task_balance_dataset():
    print(" Démarrage de l'équilibrage des classes (Limite: 1000)...")
    limit = 1000
    os.makedirs(BALANCED_DATASET, exist_ok=True)

    for cls in os.listdir(RESIZED_DATASET):
        cls_path = os.path.join(RESIZED_DATASET, cls)
        images = os.listdir(cls_path)
        new_cls_path = os.path.join(BALANCED_DATASET, cls)
        os.makedirs(new_cls_path, exist_ok=True)

        # Sous-échantillonnage aléatoire si on dépasse la limite
        if len(images) > limit:
            images = random.sample(images, limit)

        for img in images:
            src = os.path.join(cls_path, img)
            dst = os.path.join(new_cls_path, img)
            shutil.copyfile(src, dst) 
            
    print(" Équilibrage terminé.")


def task_split_train_val_test():
    print(" Démarrage du split (70/15/15)...")
    train_ratio, val_ratio = 0.7, 0.15

    for cls in os.listdir(BALANCED_DATASET):
        cls_path = os.path.join(BALANCED_DATASET, cls)
        images = os.listdir(cls_path)
        random.shuffle(images) 

        train_end = int(len(images) * train_ratio)
        val_end = int(len(images) * (train_ratio + val_ratio))

        train_imgs = images[:train_end]
        val_imgs = images[train_end:val_end]
        test_imgs = images[val_end:]

        for split, imgs in zip(["train", "val", "test"], [train_imgs, val_imgs, test_imgs]):
            split_path = os.path.join(FINAL_SPLIT_DATASET, split, cls)
            os.makedirs(split_path, exist_ok=True)
            for img in imgs:
                src = os.path.join(cls_path, img)
                dst = os.path.join(split_path, img)
                shutil.copyfile(src, dst) 

    print(" Split terminé. Le dataset est prêt pour Entrainement !")



default_args = {
    'owner': 'data_engineer_phytoscan',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='phytoscan_dataset_preparation',
    default_args=default_args,
    description="Pipeline de préparation des images pour l'entraînement d'EfficientNet",
    schedule_interval='@monthly', 
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['phytoscan', 'etl', 'computer_vision'],
) as dag:

    t1_resize = PythonOperator(
        task_id='resize_and_clean_names',
        python_callable=task_resize_and_clean
    )

    t2_balance = PythonOperator(
        task_id='balance_dataset_undersampling',
        python_callable=task_balance_dataset
    )

    t3_split = PythonOperator(
        task_id='split_train_val_test',
        python_callable=task_split_train_val_test
    )

    t1_resize >> t2_balance >> t3_split