import os
import shutil
from random import sample

def copy_images(source_dir, target_dir, num_images):
    """
    Kopiert eine bestimmte Anzahl von Bildern aus einem Quellverzeichnis in ein Zielverzeichnis.

    Args:
        source_dir (str): Pfad zum Quellverzeichnis.
        target_dir (str): Pfad zum Zielverzeichnis.
        num_images (int): Anzahl der zu kopierenden Bilder.
    """
    # Liste aller Bilder im Quellverzeichnis erstellen
    all_images = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    # Zufällige Auswahl von Bildern
    selected_images = sample(all_images, num_images)

    # Bilder in das Zielverzeichnis kopieren
    for image in selected_images:
        shutil.copy(os.path.join(source_dir, image), target_dir)

# Beispielaufruf der Funktion
copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Train\Male', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\men", 700)
copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Test\Male', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\men", 300)
copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Train\Female', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\women", 700)
copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Test\Female', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\women", 300)

