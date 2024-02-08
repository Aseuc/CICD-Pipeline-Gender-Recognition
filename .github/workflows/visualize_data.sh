            # FILEPATH: /c:/CICDPipeline/CICD-Pipeline-Gender-Recognition/.github/workflows/workflow.yaml

            generate_report() {
                local report_file=$1
                local data_file=$2
                local distribution_type=$3

                if [ -s "$data_file" ]; then
                    echo "## Daten folgen wahrscheinlich einer $distribution_type!" > "$report_file"
                    cat "$data_file" >> "$report_file"
                else
                    echo " "
                fi
            }


            publish_additional_plots() {
                local report_file=$1

                echo "\n## Balancierte Daten Geschlechter" >> "$report_file"
                cml-publish data/plots_balanced/Gender_balanced.png

                echo "\n## Balancierte Daten Jung und Alt" >> "$report_file"
                cml-publish data/plots_balanced/Young_balanced.png
            }

            report_file_distribution="report_distribution.md"
            expoFile="data/report_data/exponential_distribution.txt"
            generate_report "$report_file_distribution" "$expoFile" "Exponentialverteilung"

            binomiaFile="data/report_data/binomia_distribution.txt"
            generate_report "$report_file_distribution" "$binomiaFile" "Binomialverteilung"

            normFile="data/report_data/norm_distribution.txt"
            generate_report "$report_file_distribution" "$normFile" "Normalverteilung"

            uniformFile="data/report_data/uniform_distribution.txt"
            generate_report "$report_file_distribution" "$uniformFile" "Uniformverteilung"

            report_file="report_data_plots.md"
            publish_plots "$report_file" "data/plot_data"

            cml-send-comment "$report_file"
            publish_additional_plots "$report_file"

# Additional code for data visualization (commented out)
# columns=$(head -n 1 data/column_source_csv/source.csv | tr ',' '\n')
# for column in $columns; do
#   echo "\n## Datenvisualisierung für $column" >> $report_file
#   cml-publish data/plot_data/${column}.png --md >> $report_file
# done



