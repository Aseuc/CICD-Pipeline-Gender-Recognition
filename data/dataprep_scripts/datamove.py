# import os
# import shutil
# from random import sample

# def copy_images(source_dir, target_dir, num_images):
#     """
#     Kopiert eine bestimmte Anzahl von Bildern aus einem Quellverzeichnis in ein Zielverzeichnis.

#     Args:
#         source_dir (str): Pfad zum Quellverzeichnis.
#         target_dir (str): Pfad zum Zielverzeichnis.
#         num_images (int): Anzahl der zu kopierenden Bilder.
#     """
#     # Liste aller Bilder im Quellverzeichnis erstellen
#     all_images = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

#     # Zufällige Auswahl von Bildern
#     selected_images = sample(all_images, num_images)

#     # Bilder in das Zielverzeichnis kopieren
#     for image in selected_images:
#         shutil.copy(os.path.join(source_dir, image), target_dir)

# # Beispielaufruf der Funktion
# copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Train\Male', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\men", 700)
# copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Test\Male', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\men", 300)
# copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Train\Female', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\women", 700)
# copy_images(r'C:\Users\busse\Desktop\Gender Classification\Dataset\Test\Female', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\women", 300)

# import os
# import shutil
# from random import sample

# def split_images(source_dir, train_dir, test_dir, train_ratio=0.7):
#     """
#     Teilt die Bilder aus einem Quellverzeichnis in Trainings- und Testverzeichnisse auf.

#     Args:
#         source_dir (str): Pfad zum Quellverzeichnis.
#         train_dir (str): Pfad zum Trainingsverzeichnis.
#         test_dir (str): Pfad zum Testverzeichnis.
#         train_ratio (float): Verhältnis der Bilder, die für das Training verwendet werden sollen.
#     """
#     # Liste aller Bilder im Quellverzeichnis erstellen
#     all_images = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

#     # Anzahl der Trainings- und Testbilder berechnen
#     num_train = int(len(all_images) * train_ratio)
#     num_test = len(all_images) - num_train

#     # Zufällige Auswahl von Trainings- und Testbildern
#     train_images = sample(all_images, num_train)
#     test_images = [image for image in all_images if image not in train_images]

#     # Bilder in die entsprechenden Verzeichnisse kopieren
#     for image in train_images:
#         shutil.copy(os.path.join(source_dir, image), train_dir)
#     for image in test_images:
#         shutil.copy(os.path.join(source_dir, image), test_dir)

# # Beispielaufruf der Funktion
# split_images(r'C:\Users\busse\Desktop\adience-fold-frontal-faces\men', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\men", r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\men")
# split_images(r'C:\Users\busse\Desktop\adience-fold-frontal-faces\women', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\women", r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\women")


# import os
# import shutil
# from random import sample

# def clear_directory(dir_path):
#     """
#     Löscht alle Dateien in einem gegebenen Verzeichnis.

#     Args:
#         dir_path (str): Pfad zum Verzeichnis, das geleert werden soll.
#     """
#     for filename in os.listdir(dir_path):
#         file_path = os.path.join(dir_path, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             print('Failed to delete %s. Reason: %s' % (file_path, e))

# def split_images(source_dir, train_dir, test_dir, train_ratio=0.7):
#     """
#     Teilt die Bilder aus einem Quellverzeichnis in Trainings- und Testverzeichnisse auf.

#     Args:
#         source_dir (str): Pfad zum Quellverzeichnis.
#         train_dir (str): Pfad zum Trainingsverzeichnis.
#         test_dir (str): Pfad zum Testverzeichnis.
#         train_ratio (float): Verhältnis der Bilder, die für das Training verwendet werden sollen.
#     """
#     Leeren Sie die Zielverzeichnisse
#     clear_directory(train_dir)
#     clear_directory(test_dir)

#     Liste aller Bilder im Quellverzeichnis erstellen
#     all_images = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

#     Anzahl der Trainings- und Testbilder berechnen
#     num_train = int(len(all_images) * train_ratio)
#     num_test = len(all_images) - num_train

#     Zufällige Auswahl von Trainings- und Testbildern
#     train_images = sample(all_images, num_train)
#     test_images = [image for image in all_images if image not in train_images]

#     Bilder in die entsprechenden Verzeichnisse kopieren
#     for image in train_images:
#         shutil.copy(os.path.join(source_dir, image), train_dir)
#     for image in test_images:
#         shutil.copy(os.path.join(source_dir, image), test_dir)

# Beispielaufruf der Funktion
# split_images(r'C:\Users\busse\Desktop\adience-fold-frontal-faces\men', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\men", r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\men")
# split_images(r'C:\Users\busse\Desktop\adience-fold-frontal-faces\women', r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\women", r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\women")


# import os

# def limit_images(dir_path, max_images=1000):
#     """
#     Beschränkt die Anzahl der Bilder in einem Verzeichnis auf eine bestimmte Anzahl.

#     Args:
#         dir_path (str): Pfad zum Verzeichnis, das die Bilder enthält.
#         max_images (int): Maximale Anzahl von Bildern, die im Verzeichnis bleiben sollen.
#     """
#     Liste aller Bilder im Verzeichnis erstellen
#     all_images = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

#     Wenn es mehr Bilder gibt als max_images, lösche die überzähligen
#     if len(all_images) > max_images:
#         images_to_delete = all_images[max_images:]
#         for image in images_to_delete:
#             os.remove(os.path.join(dir_path, image))

# Beispielaufruf der Funktion
# limit_images(r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\men")
# limit_images(r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\train\women")


import os

def limit_images(dir_path, max_images=300):
    """
    Beschränkt die Anzahl der Bilder in einem Verzeichnis auf eine bestimmte Anzahl.

    Args:
        dir_path (str): Pfad zum Verzeichnis, das die Bilder enthält.
        max_images (int): Maximale Anzahl von Bildern, die im Verzeichnis bleiben sollen.
    """
    # Liste aller Bilder im Verzeichnis erstellen
    all_images = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    print(f"Found {len(all_images)} images in {dir_path}")

    # Wenn es mehr Bilder gibt als max_images, lösche die überzähligen
    if len(all_images) > max_images:
        images_to_delete = all_images[max_images:]
        print(f"Deleting {len(images_to_delete)} images")
        for image in images_to_delete:
            os.remove(os.path.join(dir_path, image))

# Beispielaufruf der Funktion
limit_images(r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\men")
limit_images(r"C:\CICDPipeline\CICD-Pipeline-Gender-Recognition\data\train-test-data\test\women")