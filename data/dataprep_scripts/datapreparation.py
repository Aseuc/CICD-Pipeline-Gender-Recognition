import os
import random
import shutil
import threading
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kstest, shapiro, uniform
import time
import psutil

class DataPreparation:
    total_images = 0
    # Variablendeklaration von Bilddateipfaden
    image_folder = "data/img_align_celeba"
    csv_path = "data/source_csv/list_attr_celeba.csv"
    source_csv_all_ids = "data/IDs/source_csv_all_ids.csv"
    source_train_path = "data/train-test-data/"
    image_source_path = "data/img_align_celeba"
    men_image_source_path_train = "data/train-test-data/train/men"
    women_image_source_path_train = "data/train-test-data/train/women"
    men_image_source_path_test = "data/train-test-data/test/men"
    women_image_source_path_test = "data/train-test-data/test/women"

    # Erstellen eines Arrays von Verzeichnissen, die für die Datenverarbeitung erforderlich sind
    required_directories = [
        source_train_path,
        women_image_source_path_test,
        men_image_source_path_test,
        men_image_source_path_train,
        women_image_source_path_train,
    ]

    # Variablendeklaration von CSV-Dateipfaden
    IDs = "data/IDs"
    male_csv = "data/IDs/male_ids.csv"
    female_csv = "data/IDs/female_ids.csv"
    data_ids = "data/IDs/data-ids.csv"

    # festlegen des identifizierenden Spaltennamens
    id_column = "image_id"

    # festlegen des Spaltennamens, der das Merkmal enthält worauf trainiert werden soll
    feature_column = "Male"

    # Variablendeklaration in dem die Visualisierungsdaten gespeichert werden
    data_vis_path = "data/plot_data"
    data_vis_path_balanced = "data/plots_balanced/"
    def run_dataprep(total_images):
        DataPreparation.create_directories()
        DataPreparation.extract_ids(
            csv_path=DataPreparation.csv_path,
            column=DataPreparation.feature_column,
            id_column=DataPreparation.id_column,
        )
        DataPreparation.clear_directory(
            dir_path=DataPreparation.men_image_source_path_test
        )
        DataPreparation.clear_directory(
            dir_path=DataPreparation.men_image_source_path_train
        )
        DataPreparation.clear_directory(
            dir_path=DataPreparation.women_image_source_path_test
        )
        DataPreparation.clear_directory(
            dir_path=DataPreparation.women_image_source_path_train
        )
        DataPreparation.split_data_random(
            image_folder=DataPreparation.image_folder,
            male_csv=DataPreparation.male_csv,
            female_csv=DataPreparation.female_csv,
            total_images=total_images,
            id_column=DataPreparation.id_column,
        )

    @staticmethod
    def create_directories():
        os.makedirs(DataPreparation.men_image_source_path_train, exist_ok=True)
        os.makedirs(DataPreparation.women_image_source_path_train, exist_ok=True)
        os.makedirs(DataPreparation.women_image_source_path_test, exist_ok=True)
        os.makedirs(DataPreparation.men_image_source_path_test, exist_ok=True)
        os.makedirs(DataPreparation.IDs, exist_ok=True)

    @staticmethod
    def extract_ids_source_data_and_save(
        directory, csv_path="data-ids.csv", id_column="image_id"
    ):
        filenames = os.listdir(directory)
        df = pd.DataFrame(filenames, columns=[id_column])
        df.to_csv(csv_path, index=False)

    @staticmethod
    def extract_all_ids(csv_path, column="Male", id_column="image_id"):
        df = pd.read_csv(csv_path)
        df[column] = df[column].replace(-1, 0)
        df.to_csv(f"data/IDs/source_csv_all_ids.csv", columns=[id_column], index=False)

    @staticmethod
    def extract_ids(csv_path, column="Male", id_column="image_id"):
        df = pd.read_csv(csv_path)
        df[column] = df[column].replace(-1, 0)
        male_df = df[df[column] == 1]
        female_df = df[df[column] == 0]
        male_df.to_csv(f"data/IDs/male_ids.csv", columns=[id_column], index=False)
        female_df.to_csv(f"data/IDs/female_ids.csv", columns=[id_column], index=False)

    @staticmethod
    def clear_directory(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))

    @staticmethod
    def get_ids_from_csv(csv_file, id_column):
        df = pd.read_csv(csv_file)
        ids = df[id_column].tolist()
        return ids

    @staticmethod
    def split_data_random(
        image_folder, male_csv, female_csv, total_images, id_column, train_ratio=0.7
    ):
        male_ids = DataPreparation.get_ids_from_csv(male_csv, id_column)
        female_ids = DataPreparation.get_ids_from_csv(female_csv, id_column)

        num_train = int(total_images * train_ratio)
        num_test = int(total_images - num_train)

        test_ids_male = random.sample(male_ids, num_test // 2)
        test_ids_female = random.sample(female_ids, num_test // 2)
        test_ids = test_ids_male + test_ids_female

        train_ids_male = set(male_ids) - set(test_ids)
        train_ids_female = set(female_ids) - set(test_ids)
        male_ids = sorted(train_ids_male)
        female_ids = sorted(train_ids_female)
        female_ids = random.sample(female_ids, num_train // 2)
        male_ids = random.sample(male_ids, num_train // 2)

        for id in test_ids_male:
            shutil.copy(
                os.path.join(image_folder, id),
                DataPreparation.men_image_source_path_test,
            )

        for id in test_ids_female:
            shutil.copy(
                os.path.join(image_folder, id),
                DataPreparation.women_image_source_path_test,
            )

        for id in male_ids:
            shutil.copy(
                os.path.join(image_folder, id),
                DataPreparation.men_image_source_path_train,
            )

        for id in female_ids:
            shutil.copy(
                os.path.join(image_folder, id),
                DataPreparation.women_image_source_path_train,
            )


class DataTest:
    """
    Eine Klasse, die verschiedene Tests und Überprüfungen auf den Daten durchführt.

    Attributes:
        save_norm_distribution_path_txt (str): Der Pfad zum Speichern der Normalverteilungsdaten.
        save_binomial_distribution_path_txt (str): Der Pfad zum Speichern der Binomialverteilungsdaten.
        save_uniform_distribution_path_txt (str): Der Pfad zum Speichern der Gleichverteilungsdaten.
        save_exponential_distribution_path_txt (str): Der Pfad zum Speichern der Exponentialverteilungsdaten.
    """
     
    save_norm_distribution_path_txt = ""
    save_binomial_distribution_path_txt = ""
    save_uniform_distribution_path_txt = ""
    save_exponential_distribution_path_txt = ""


    """
        Führt verschiedene Tests und Überprüfungen auf den Daten aus.

        Args:
            save_binomial_distribution_path_txt (str): Der Pfad zum Speichern der Binomialverteilungsdaten.
            save_uniform_distribution_path_txt (str): Der Pfad zum Speichern der Gleichverteilungsdaten.
            save_exponential_distribution_path_txt (str): Der Pfad zum Speichern der Exponentialverteilungsdaten.
            save_norm_distribution_path_txt (str): Der Pfad zum Speichern der Normalverteilungsdaten.

        Returns:
            None
    """
    def run_datatest(
        save_binomial_distribution_path_txt,
        save_uniform_distribution_path_txt,
        save_exponential_distribution_path_txt,
        save_norm_distribution_path_txt,
    ):
        DataPreparation.create_directories()
        DataPreparation.extract_ids_source_data_and_save(
            directory=DataPreparation.image_folder, csv_path=DataPreparation.data_ids
        )
        DataPreparation.extract_all_ids(
            csv_path=DataPreparation.csv_path,
            column=DataPreparation.feature_column,
            id_column=DataPreparation.id_column,
        )

        DataTest.check_data_completeness(
            csv1=DataPreparation.data_ids, csv2=DataPreparation.source_csv_all_ids
        )

        DataTest.test_image_extensions(directory=DataPreparation.image_folder)

        DataTest.check_csv_extension(csv_path=DataPreparation.csv_path)

        DataTest.check_required_directories_data_exists(
            directories=DataPreparation.required_directories
        )

        DataTest.test_quality_of_csv(
            csv_path=DataPreparation.csv_path,
            column_name_of_image_paths=DataPreparation.id_column,
        )

        DataTest.test_outliers_zscore(csv_path=DataPreparation.csv_path)

        DataTest.test_outliers_IQR(df=pd.read_csv(DataPreparation.csv_path))

        DataTest.test_balance_all_columns(csv_path=DataPreparation.csv_path)

        DataTest.detect_anomaly(
            csv_path=DataPreparation.csv_path, id_column=DataPreparation.id_column
        )
        stat, p = DataTest.test_image_brightness(
            source_directory=DataPreparation.image_folder, num_images=3, num_pixels=1000
        )
        print(
            f"Kruskal-Wallis-Test result: {stat}, p-value: {p}. A small p-value (typically less than 0.05) indicates that there is likely a significant difference in the brightness values of the selected images."
        )

        DataTest.test_normal_distribution(
            data=DataPreparation.csv_path,
            save_distribution_path_txt=save_norm_distribution_path_txt,
        )

        DataTest.test_uniform_distribution(
            data=DataPreparation.csv_path,
            save_distribution_path_txt=save_uniform_distribution_path_txt,
        )

        DataTest.test_binomial_distribution(
            csv_path=DataPreparation.csv_path,
            save_distribution_path_txt=save_binomial_distribution_path_txt,
            p=0.5,
        )

        DataTest.test_exponential_distribution(
            csv_path=DataPreparation.csv_path,
            save_distribution_path_txt=save_exponential_distribution_path_txt,
        )

    @staticmethod
    def check_data_completeness(csv1, csv2):
        df1 = pd.read_csv(csv1)
        df2 = pd.read_csv(csv2)
        column1 = set(df1.iloc[:, 0])
        column2 = set(df2.iloc[:, 0])
        missing_in_1 = column1.difference(column2)
        missing_in_2 = column2.difference(column1)
        if missing_in_1:
            print(
                f"::warning:: Die folgenden IDs fehlen in der zweiten Datei: {missing_in_1}"
            )
        if missing_in_2:
            print(
                f"::warning:: Die folgenden IDs fehlen in der ersten Datei: {missing_in_2}"
            )
        is_equal = len(missing_in_1) == 0 and len(missing_in_2) == 0
        if is_equal:
            print(
                "::warning:: Daten sind vollständig! Die Bilddaten-IDs stimmen mit den IDs aus Attributliste überein! "
            )
        else:
            print(
                "::warning:: Die Bilddaten-IDs stimmen nicht mit den IDs aus der Attributliste überein! "
            )
            assert False
        return is_equal

    @staticmethod
    def is_numeric(column):
        try:
            pd.to_numeric(column)
            return True
        except ValueError:
            return False

    @staticmethod
    def test_image_extensions(directory):
        filenames = os.listdir(directory)
        valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
        invalid_files = [
            file
            for file in filenames
            if os.path.splitext(file)[1].lower() not in valid_extensions
        ]

        if len(invalid_files) > 0:
            print(
                f"Ungültige Dateierweiterungen gefunden in den Dateien: {invalid_files}"
            )

        assert (
            len(invalid_files) == 0
        ), f"Nicht alle Dateien im Verzeichnis {directory} sind Bilddateien. Überprüfe die Dateierweiterungen."

    @staticmethod
    def check_csv_extension(csv_path):
        _, ext = os.path.splitext(csv_path)
        assert ext.lower() == ".csv", f"Die Datei {csv_path} hat keine .csv Erweiterung"

    @staticmethod
    def check_required_directories_data_exists(directories):
        for directory in directories:
            assert os.path.isdir(
                directory
            ), f"Das Verzeichnis {directory} existiert nicht"

    @staticmethod
    def test_quality_of_csv(csv_path, column_name_of_image_paths="image_id"):
        df = pd.read_csv(csv_path)
        assert (
            df[column_name_of_image_paths].isnull().sum() == 0
        ), f"Es gibt fehlende Werte in der Spalte {column_name_of_image_paths}"
        assert df.duplicated().sum() == 0, "Es gibt Duplikate in den Daten"

    @staticmethod
    def test_outliers_zscore(csv_path):
        df = pd.read_csv(csv_path)
        for column_name in df.columns:
            if np.issubdtype(
                df[column_name].dtype, np.number
            ):  # Überprüfe, ob die Spalte numerisch ist
                z_scores = np.abs(
                    (df[column_name] - df[column_name].mean()) / df[column_name].std()
                )
                if any(z_scores > 3):
                    print(f"::warning::Es gibt Ausreißer in der Spalte '{column_name}'")

    @staticmethod
    def test_balance_all_columns(csv_path):
        """
        Überprüft das Gleichgewicht aller Spalten in einer CSV-Datei.

        Args:
            csv_path (str): Der Pfad zur CSV-Datei.

        Returns:
            None

        """
        df = pd.read_csv(csv_path)
        imbalance_report = []

        for column_name in df.columns:
            if DataTest.is_numeric(df[column_name]) == True:
                if np.issubdtype(
                    df[column_name].dtype, np.number
                ):  # Überprüfe, ob die Spalte numerisch ist
                    counts = df[column_name].value_counts()
                    if abs(counts.get(-1, 0) - counts.get(1, 0)) >= 0.1 * len(df):
                        imbalance_report.append(
                            f"Die Spalte '{column_name}' ist unausgeglichen. Anzahl von -1: {counts.get(-1, 0)}, Anzahl von 1: {counts.get(1, 0)}"
                        )
        if imbalance_report:
            print("Es gibt unausgeglichene Spalten:\n" + "\n".join(imbalance_report))

    @staticmethod
    def test_outliers_IQR(df):
        """
        Berechnet den Prozentsatz der Ausreißer für numerische Spalten eines DataFrame unter Verwendung des IQR-Verfahrens.

        Parameters:
            df (pandas.DataFrame): Der DataFrame, für den die Ausreißer berechnet werden sollen.

        Returns:
            dict: Ein Wörterbuch, das den Prozentsatz der Ausreißer für jede numerische Spalte enthält.
        """
        outliers_percentage = {}
        for column_name in df.columns:
            if pd.api.types.is_numeric_dtype(df[column_name]):
                Q1 = df[column_name].quantile(0.25)
                Q3 = df[column_name].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[
                    (df[column_name] < lower_bound) | (df[column_name] > upper_bound)
                ]
                outliers_percentage[column_name] = len(outliers) / len(df) * 100
                print(
                    f"Ausreißerprozentwert für Spalte '{column_name}': {outliers_percentage[column_name]}%"
                )

        return outliers_percentage

    @staticmethod
    def detect_outliers(df, column_name):
        """
        Erkennt Ausreißer in einer gegebenen Spalte eines DataFrame.

        Parameters:
            df (pandas.DataFrame): Der DataFrame, in dem die Ausreißer erkannt werden sollen.
            column_name (str): Der Name der Spalte, in der die Ausreißer erkannt werden sollen.

        Returns:
            pandas.DataFrame: Ein DataFrame, der nur die Ausreißer enthält.
        """
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)]
        return outliers

    @staticmethod
    def detect_anomaly(csv_path, id_column):
        """
        Erkennt Anomalien in den Daten.

        :param csv_path: Der Pfad zur CSV-Datei mit den Daten.
        :type csv_path: str
        :param id_column: Der Name der Spalte, die die IDs enthält.
        :type id_column: str
        :raises ValueError: Wenn Anomalien in den Daten gefunden werden.
        """
        from sklearn.ensemble import IsolationForest

        X = pd.read_csv(csv_path)
        X = X.drop(id_column, axis=1)
        clf = IsolationForest(random_state=0).fit(X)
        y_pred = clf.predict(X)
        if -1 not in y_pred or 1 not in y_pred:
            raise ValueError("Anomalie gefunden!")
        print("Keine Anomalien gefunden.")

    @staticmethod
    def test_normal_distribution(
        data, save_distribution_path_txt="data/reports_data/norm_distribution.txt"
    ):
        """
        Überprüft, ob die Daten in einem DataFrame einer Normalverteilung folgen.

        Parameters:
            data (str): Der Pfad zur CSV-Datei, die die Daten enthält.
            save_distribution_path_txt (str, optional): Der Pfad zur Textdatei, in der die Ergebnisse gespeichert werden sollen. Standardmäßig "data/reports_data/norm_distribution.txt".

        Returns:
            None
        """
        df = pd.read_csv(data)
        results = []
        for column_name in df.columns:
            if pd.api.types.is_numeric_dtype(df[column_name]):
                stat, p = shapiro(df[column_name])
                if p > 0.05:
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich einer Normalverteilung."
                    print(result)
                else:
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich nicht einer Normalverteilung."
                    print(result)
                results.append(result)
        with open(f"{save_distribution_path_txt}", "w") as f:
            for result in results:
                f.write(f"{result}\n")

    @staticmethod
    def test_uniform_distribution(
        data, save_distribution_path_txt="data/reports_data/uniform_distribution.txt"
    ):
        """
        Überprüft, ob die Daten in einem DataFrame eine gleichmäßige Verteilung aufweisen.

        Parameters:
            data (str): Der Pfad zur CSV-Datei, die die Daten enthält.
            save_distribution_path_txt (str, optional): Der Pfad zur Textdatei, in der die Ergebnisse gespeichert werden sollen. Standardmäßig "data/reports_data/uniform_distribution.txt".

        Returns:
            None
        """
        df = pd.read_csv(data)
        results = []
        for column_name in df.columns:
            if pd.api.types.is_numeric_dtype(df[column_name]):
                theoretical_values = uniform.rvs(size=len(df))
                stat, p = kstest(df[column_name], theoretical_values)
                if p > 0.05:
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich einer Uniformverteilung."
                    print(result)
                else:
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich nicht einer Uniformverteilung."
                    print(result)
                results.append(result)

        with open(f"{save_distribution_path_txt}", "w") as f:
            for result in results:
                f.write(f"{result}\n")

    @staticmethod
    def test_binomial_distribution(
        csv_path,
        save_distribution_path_txt="data/reports_data/binomial_distribution.txt",
        p=0.5,
    ):
        """
        Überprüft, ob die Daten in einer CSV-Datei einer Binomialverteilung folgen.

        Parameter:
            csv_path (str): Der Pfad zur CSV-Datei.
            save_distribution_path_txt (str, optional): Der Pfad zur Textdatei, in der die Ergebnisse gespeichert werden sollen. Standardmäßig "data/reports_data/binomial_distribution.txt".
            p (float, optional): Der Erfolgswahrscheinlichkeitsparameter der Binomialverteilung. Standardmäßig 0.5.

        Returns:
            None
        """
        df = pd.read_csv(csv_path)
        results = []
        for column_name in df.columns:
            if pd.api.types.is_numeric_dtype(df[column_name]):
                data = df[column_name].replace(-1, 0)
                value_counts = data.value_counts()
                observed_values = [value_counts.get(1, 0), value_counts.get(0, 0)]
                n = len(data)

                expected_values = [n * p, n * (1 - p)]

                if (
                    abs(observed_values[0] - expected_values[0]) / n < 0.05
                    and abs(observed_values[1] - expected_values[1]) / n < 0.05
                ):
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich einer Binomial-Verteilung."
                    print(result)
                else:
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich nicht einer Binomial-Verteilung."
                    print(result)
                results.append(result)

        with open(save_distribution_path_txt, "w") as f:
            for result in results:
                f.write(f"{result}\n")

    @staticmethod
    def test_exponential_distribution(
        csv_path,
        save_distribution_path_txt="data/reports_data/exponential_distribution.txt",
    ):
        """
        Überprüft, ob die Daten in einer CSV-Datei einer Exponentialverteilung folgen.

        Parameter:
            csv_path (str): Der Pfad zur CSV-Datei.
            save_distribution_path_txt (str, optional): Der Pfad zur Textdatei, in der die Ergebnisse gespeichert werden sollen. Standardmäßig "data/reports_data/exponential_distribution.txt".

        Returns:
            None
        """
        df = pd.read_csv(csv_path)
        results = []
        for column_name in df.columns:
            if pd.api.types.is_numeric_dtype(df[column_name]):
                # Entfernen Sie nicht-numerische Werte
                data = df[column_name].dropna()
                stat, p_value = kstest(data, "expon")
                if p_value > 0.05:
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich einer Exponentialverteilung."
                    print(result)
                else:
                    result = f"Die Daten in der Spalte {column_name} folgen wahrscheinlich nicht einer Exponentialverteilung."
                    print(result)
                results.append(result)

        with open(save_distribution_path_txt, "w") as f:
            for result in results:
                f.write(f"{result}\n")

    @staticmethod
    def test_image_brightness(source_directory, num_images=3, num_pixels=1000):
        """
        Berechnet die Helligkeit von zufällig ausgewählten Bildern im angegebenen Verzeichnis.

        :param source_directory: Das Verzeichnis, in dem die Bilder gespeichert sind.
        :type source_directory: str
        :param num_images: Die Anzahl der zufällig ausgewählten Bilder, die verwendet werden sollen. Standardwert ist 3.
        :type num_images: int
        :param num_pixels: Die Anzahl der zufällig ausgewählten Pixel pro Bild, die zur Berechnung der Helligkeit verwendet werden sollen. Standardwert ist 1000.
        :type num_pixels: int
        :return: Ein Tupel bestehend aus dem Statistikwert und dem p-Wert des Kruskal-Wallis-Tests.
        :rtype: tuple
        """
        from PIL import Image
        from scipy.stats import kruskal

        image_files = [f for f in os.listdir(source_directory) if f.endswith(".jpg")]

        # Zufällige Auswahl von Bildern
        selected_images = random.sample(image_files, num_images)

        # Liste zur Speicherung der Helligkeitswerte
        brightness_values = []

        for image_file in selected_images:
            img = Image.open(os.path.join(source_directory, image_file)).convert("L")
            img_array = np.array(img)
            pixel_indices = random.sample(range(img_array.size), num_pixels)
            selected_pixels = img_array.ravel()[pixel_indices]
            brightness_values.append(selected_pixels)
        stat, p = kruskal(*brightness_values)
        return stat, p


class DataBalancing:
    """
    Diese Klasse bietet Methoden zum Ausgleichen von Daten in einer CSV-Datei.

    Methoden:
    - balance_column(csv_path, column_name): Gleicht die Daten in der angegebenen Spalte der CSV-Datei aus.
    """

    def balance_column(csv_path, column_name):
        """
        Gleicht die Daten in der angegebenen Spalte der CSV-Datei aus.

        Args:
        - csv_path (str): Der Pfad zur CSV-Datei.
        - column_name (str): Der Name der auszugleichenden Spalte.

        Returns:
        - df_balanced (pandas.DataFrame): Der ausgeglichene DataFrame.
        """
        df = pd.read_csv(csv_path)
        counts = df[column_name].value_counts()
        min_count = min(counts.get(-1, 0), counts.get(1, 0))
        df_balanced = pd.concat(
            [
                df[df[column_name] == -1].sample(min_count),
                df[df[column_name] == 1].sample(min_count),
            ],
            axis=0,
        )
        return df_balanced


class DataVisualization:
    """
    Eine Klasse zur Datenvisualisierung.

    Attributes:
        balanced_gender_path (str): Der Pfad zur gespeicherten ausgeglichenen Gender-Datei.
        balanced_young_path (str): Der Pfad zur gespeicherten ausgeglichenen Young-Datei.
    """

    balanced_gender_path = ""
    balanced_young_path = ""

    def run_datavis(
        balanced_gender_path, balanced_young_path, column_name, feature_column
    ):
        """
        Führt die Datenvisualisierung aus.

        Args:
            balanced_gender_path (str): Der Pfad zur gespeicherten ausgeglichenen Gender-Datei.
            balanced_young_path (str): Der Pfad zur gespeicherten ausgeglichenen Young-Datei.
            column_name (str): Der Name der Spalte für die Auswertung.
            feature_column (str): Der Name der Merkmals-Spalte.

        Returns:
            None
        """
        DataVisualization.histogram_all_columns(
            DataPreparation.csv_path, DataPreparation.data_vis_path
        )
        df_balanced_gender = DataBalancing.balance_column(
            csv_path=DataPreparation.csv_path,
            column_name=DataPreparation.feature_column,
        )
        df_balanced_gender.to_csv(balanced_gender_path, index=False)
        DataVisualization.plot_histogram(
            df=df_balanced_gender,
            column_name=DataPreparation.feature_column,
            title="Ausgeglichene Verteilung der Geschlechter",
            save_path=DataPreparation.data_vis_path_balanced,
            save_name="balanced_gender",
        )
        df_balanced_young = DataBalancing.balance_column(
            csv_path=DataPreparation.csv_path, column_name=column_name
        )
        df_balanced_young.to_csv(balanced_young_path, index=False)
        DataVisualization.plot_histogram(
            df=df_balanced_young,
            column_name=DataPreparation.feature_column,
            title="Ausgeglichene Verteilung von Jung und Alt",
            save_path=DataPreparation.data_vis_path_balanced,
            save_name="balanced_young",
        )

    def plot_histogram(df, column_name, title, save_path, save_name):
        """
        Erstellt ein Histogramm für eine gegebene Spalte und speichert es ab.

        Args:
            df (pandas.DataFrame): Der DataFrame, der die Daten enthält.
            column_name (str): Der Name der Spalte.
            title (str): Der Titel des Histogramms.
            save_path (str): Der Pfad zum Speichern des Histogramms.
            save_name (str): Der Name des gespeicherten Histogramms.

        Returns:
            None
        """
        counts = df[column_name].value_counts()
        plt.bar(
            [f"nicht {column_name}", f"{column_name}"],
            [counts[-1], counts[1]],
            color=["#ff69b4", "#1f77b4"],
        )
        for i, v in enumerate([counts[-1], counts[1]]):
            plt.text(i, v, str(v), fontsize=12, ha="center", va="bottom")
        plt.title(title)
        plt.xlabel(f"{column_name} oder nicht {column_name}")
        plt.ylabel("Anzahl")
        plt.savefig(f"{save_path}/{save_name}.png")
        # plt.show()
        plt.clf()

    def histogram_all_columns(csv_path, save_path):
        """
        Erstellt Histogramme für alle Spalten im gegebenen CSV und speichert sie ab.

        Args:
            csv_path (str): Der Pfad zur CSV-Datei.
            save_path (str): Der Pfad zum Speichern der Histogramme.

        Returns:
            None
        """
        df = pd.read_csv(csv_path)
        for column_name in df.columns:
            if np.issubdtype(
                df[column_name].dtype, np.number
            ):  # Überprüfe, ob die Spalte numerisch ist
                counts = df[column_name].value_counts()
                counts.plot(
                    kind="bar",
                    title=f"Verteilung der Werte in der Spalte '{column_name}'",
                )
                plt.savefig(f"{save_path}/{column_name}.png")
                # plt.show()
                plt.clf()


class Main(DataPreparation, DataTest, DataBalancing, DataVisualization):
    """
    Die Hauptklasse, die die verschiedenen Funktionen zur Datenverarbeitung, Datenprüfung, Datenbalancierung und Datenvisualisierung enthält.
    """
    def __init__(self):
            """
            Initialisiert eine Instanz der Klasse DataPreparation.

            Die Methode initialisiert die Attribute der Klasse, einschließlich der Anzahl der Gesamtbilder,
            der Pfade zu den ausbalancierten CSV-Dateien, der Spaltennamen für das Alter, der Pfade zu den
            Ausgabedateien für die Verteilungsberichte, der Listen für den Speicher- und CPU-Verbrauch,
            der Zeitstempel und der Thread-Steuerungsvariablen.

            Parameter:
            - self: Die Instanz der Klasse DataPreparation.

            Rückgabewert:
            - None
            """
            self.total_images = 2000
            self.balanced_gender_path = "data/balanced_source_csv/gender_balanced.csv"
            self.balanced_young_path = "data/balanced_source_csv/young_balanced.csv"
            self.young_column = "Young"
            self.save_norm_distribution_path_txt = "data/reports_data/norm_distribution.txt"
            self.save_binomial_distribution_path_txt = "data/reports_data/binomial_distribution.txt"
            self.save_uniform_distribution_path_txt = "data/reports_data/uniform_distribution.txt"
            self.save_exponential_distribution_path_txt = (
                "data/reports_data/exponential_distribution.txt"
            )
            self.memory_usage = []
            self.cpu_usage = []
            self.timestamps = []
            self.stop_thread = False
            self.thread = threading.Thread(target=self.collect_usage)
            self.time = 0
    def collect_usage(self):
            """
            Sammelt die CPU- und Speicherauslastung in regelmäßigen Abständen.

            Diese Methode läuft in einer Schleife, bis der stop_thread-Flag gesetzt ist.
            In jedem Schleifendurchlauf werden die CPU-Auslastung, die Speicherauslastung
            und der Zeitstempel erfasst und in den entsprechenden Listen gespeichert.

            Args:
                self: Die Instanz der Klasse.

            Returns:
                None
            """
            while not self.stop_thread:
                self.memory_usage.append(psutil.virtual_memory().percent)
                self.cpu_usage.append(psutil.cpu_percent(interval=1))
                self.timestamps.append(time.time())
                time.sleep(1)
            print(self.cpu_usage, self.memory_usage, self.timestamps)

    def run_all(self):
            """
            Führt alle Schritte der Datenverarbeitung aus, einschließlich der Ausführung von DataTest, DataVisualization und DataPreparation.
            """
            self.thread.start()
            start_time = time.time()
            DataTest.run_datatest(
                self.save_binomial_distribution_path_txt,
                self.save_uniform_distribution_path_txt,
                self.save_exponential_distribution_path_txt,
                self.save_norm_distribution_path_txt,
            )
            DataVisualization.run_datavis(
                balanced_gender_path=self.balanced_gender_path,
                balanced_young_path=self.balanced_young_path,
                column_name=self.young_column,
                feature_column=DataPreparation.feature_column,
            )

            DataPreparation.run_dataprep(total_images=self.total_images)
            
            self.stop_thread = True
            self.thread.join()
            self.plot_usage()


    def get_usage_collection(self):
            """
            Gibt die CPU-Auslastung, den Speicherverbrauch und die Zeitstempel zurück.

            Returns:
                Tuple: Ein Tupel bestehend aus der CPU-Auslastung, dem Speicherverbrauch und den Zeitstempeln.
            """
            return self.cpu_usage, self.memory_usage, self.timestamps
    
    def plot_usage(self):
        """
        Plottet die CPU- und Speichernutzung während der Datenvorbereitung.

        :return: None
        """
        cpu_usage, memory_usage, timestamps = self.get_usage_collection()
        plt.title("CPU und Speichernutzung während der Datenvorbereitung")
        plt.xlabel("Zeit (s)")
        plt.ylabel("Nutzung (%)")
        plt.legend(["CPU-Nutzung", "Speichernutzung"])
        # plt.figure(facecolor="lightgrey")
        plt.plot(timestamps, cpu_usage, label="CPU Auslastung", color="red", linewidth=3)
        plt.plot(timestamps, memory_usage, label="Speicher Nutzung", color="blue",linewidth=3)
        plt.savefig("data/cpu_memory_usage_on_dataprep.png")
        plt.show()

if __name__ == "__main__":
    main = Main()
    main.run_all()
    