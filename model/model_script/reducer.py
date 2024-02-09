import os
import random
import shutil

def reduce_image_data(source_dir, num_images_to_keep):
    # Liste aller Bilddateien im Verzeichnis
    all_images = [f for f in os.listdir(source_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Überprüfen, ob die Anzahl der zu behaltenden Bilder kleiner ist als die Gesamtzahl
    if num_images_to_keep < len(all_images):
        # Zufällige Auswahl von Bildern, die behalten werden sollen
        images_to_keep = random.sample(all_images, num_images_to_keep)

        # Löschen der Bilder, die nicht in der Liste der zu behaltenden Bilder sind
        for image in all_images:
            if image not in images_to_keep:
                os.remove(os.path.join(source_dir, image))

# Verwendung der Funktion
source_dir = r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\new_test_dataset\train-test-data\test\men"
num_images_to_keep = 250  # Anzahl der zu behaltenden Bilder
reduce_image_data(source_dir, num_images_to_keep)