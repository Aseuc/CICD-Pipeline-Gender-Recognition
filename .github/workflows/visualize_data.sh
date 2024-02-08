            # FILEPATH: /c:/CICDPipeline/CICD-Pipeline-Gender-Recognition/.github/workflows/workflow.yaml

            # Dieser Abschnitt des Codes generiert eine Berichtsdatei mit Informationen zur Verteilung der Daten.
            # Es wird überprüft, ob bestimmte Dateien existieren und ob sie nicht leer sind. Wenn dies der Fall ist, werden die entsprechenden Informationen an die Berichtsdatei angehängt.
            # Die Berichtsdatei wird dann veröffentlicht und ein Kommentar mit der Berichtsdatei wird gesendet.

            report_file_distribution="report_distribution.md"
            expoFile="data/report_data/exponential_distribution.txt"
            if [ -s "$file" ]
            then
              echo "## Daten folgen wahrscheinlich einer Exponentialverteilung!" > $report_file_distribution
              cat $expoFile >> $report_file_distribution
            else
              echo " "
            fi

            binomiaFile="data/report_data/binomia_distribution.txt"
            if [ -s "$file" ]
            then
              echo "## Daten folgen wahrscheinlich einer Binomialverteilung!" > $report_file_distribution
              cat $binomiaFile >> $report_file_distribution
            else
              echo " "
            fi

            normFile="data/report_data/norm_distribution.txt"
            if [ -s "$file" ]
            then
              echo "## Daten folgen wahrscheinlich einer Normalverteilung!" > $report_file_distribution
              cat $normFile >> $report_file_distribution
            else
              echo " "
            fi

            uniformFile="data/report_data/uniform_distribution.txt"
            if [ -s "$file" ]
            then
              echo "## Daten folgen wahrscheinlich einer Uniformverteilung!" > $report_file_distribution
              cat $uniformFile >> $report_file_distribution
            else
              echo " "
            fi

            report_file="report_data_plots.md"
            echo "## Modellmetriken mit verauschten Bilder" > $report_file

            # Iteriere über jede Plot-Datei im Verzeichnis data/plot_data und veröffentliche sie in der Berichtsdatei.
            for file in data/plot_data/*.png; do
              echo "Veröffentliche $file"
              cml-publish "$file" --md >> $report_file
            done

            # Sende einen Kommentar mit der Berichtsdatei.
            cml-send-comment $report_file

            # Zusätzlicher Code für die Datenvisualisierung (auskommentiert)
            # columns=$(head -n 1 data/column_source_csv/source.csv | tr ',' '\n')
            # for column in $columns; do
            #   echo "\n## Datenvisualisierung für $column" >> $report_file
            #   cml-publish data/plot_data/${column}.png --md >> $report_file
            # done

            # Append additional plots to the report file.
            echo "\n## Balancierte Daten Geschlechter" >> $report_file
            cml-publish data/plots_balanced/Gender_balanced.png

            echo "\n## Balancierte Daten Jung und Alt" >> $report_file
            cml-publish data/plots_balanced/Young_balanced.png

            # Send a comment with the updated report file.
            cml-send-comment $report_file