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

            visualize_data() {
                local report_file=$1
                local plot_data_dir=$2
                if [ -n "$(ls -A $plot_data_dir)" ]; then
                    for file in $plot_data_dir/*; do
                        echo "\n## Datenvisualisierung für $(basename "$file" .png)" >> "$report_file"
                        cml-publish "$file" --md >> "$report_file"
                    done
                fi
            }

            report_file_distribution="report_datap_plots.md"
            expoFile="data/report_data/exponential_distribution.txt"
            generate_report "$report_file_distribution" "$expoFile" "Exponentialverteilung"

            binomiaFile="data/report_data/binomia_distribution.txt"
            generate_report "$report_file_distribution" "$binomiaFile" "Binomialverteilung"

            normFile="data/report_data/norm_distribution.txt"
            generate_report "$report_file_distribution" "$normFile" "Normalverteilung"

            uniformFile="data/report_data/uniform_distribution.txt"
            generate_report "$report_file_distribution" "$uniformFile" "Uniformverteilung"

            report_file="report_data_plots.md"
            visualize_data "$report_file" "data/plot_data"
            
            report_file="report_data_plots.md"
            visualize_data "$report_file" "data/plots_balanced"
            
            cml-send-comment "$report_file"
   

# Additional code for data visualization (commented out)
# columns=$(head -n 1 data/column_source_csv/source.csv | tr ',' '\n')
# for column in $columns; do
#   echo "\n## Datenvisualisierung für $column" >> $report_file
#   cml-publish data/plot_data/${column}.png --md >> $report_file
# done



