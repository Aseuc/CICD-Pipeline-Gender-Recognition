publish_model_metrics() {
    echo "## Model Metriken" > report_ml.md
    cat test/metrics/metrics.txt >> report_ml.md
    cml-publish "test/metrics/metrics.jpg" --md >> report_ml.md
    # cml-send-comment report_ml.md
}

publish_model_fairness_metrics(){
    echo "\n## Fairlearn Ergebnisse" >> report_ml.md
    cml-publish "test/metricsFairlearn/Fig1metricsFairLearn.jpg" --md >> report_ml.md
    cml-publish "test/metricsFairlearn/Fig2metricsFairLearn.jpg" --md >> report_ml.md
    # cml-send-comment report_ml.md
}

publish_model_metrics_noise(){
            local report_file=$1
            local noise_plot_data_dir=$2
            if [ -n "$(ls -A "$noise_plot_data_dir")" ]; then
                echo "## Modellmetriken mit verauschten Bilder" > "$report_file"
                for file in "$noise_plot_data_dir"/*.png; do
                    echo "Veröffentlichung $file"
                    cml-publish "$file" --md >> "$report_file"
                done
                cml-send-comment "$report_file"
            fi
            
}
publish_model_metrics_disortion(){
    local report_file=$1
    local distortion_plot_data_dir=$2
    if [ -n "$(ls -A "$distortion_plot_data_dir")" ]; then
        echo "## Modellmetriken mit verzerrten Bildern" > "$report_file"
        for file in "$distortion_plot_data_dir"/*.png; do
            echo "Veröffentlichung $file"
            cml-publish "$file" --md >> "$report_file"
        done
        cml-send-comment "$report_file"
    fi
            
}

publish_metrics() {
    publish_model_metrics
    publish_model_fairness_metrics
    publish_model_metrics_disortion "report_ml.md" "test/test-plots-verzerrung" # Added the missing function call
}

publish_metrics 
publish_model_metrics_noise "report_ml.md" "test/test-plots-rauschen"
publish_model_metrics_disortion "report_ml.md" "test/test-plots-verzerrung"
publish_model_metrics_rotation "report_ml.md" "test/test-plots-verdrehung"


    publish_model_metrics_rotation(){
        local report_file=$1
        local rotation_plot_data_dir=$2
        if [ -n "$(ls -A "$rotation_plot_data_dir")" ]; then
            echo "## Modellmetriken mit verdrehten Bildern" > "$report_file"      
            for file in "$rotation_plot_data_dir"/*.png; do
                echo "Publishing $file"
                cml-publish "$file" --md >> "$report_file"
            done
            cml-send-comment "$report_file"
        fi
    }


           
publish_activation_map() {
  report_file_activation="report_activation.md"
  activation_map_dir="test/activation_map/"

  if [ -n "$(ls -A "$activation_map_dir")" ]; then
    echo "## Erklärbarkeit des Modells" > $report_file_activation
    for file in $activation_map_dir*.png; do
      echo "Publishing $file"
      cml-publish "$file" --md >> $report_file_activation
    done
    cml-send-comment $report_file_activation
  else
    echo "Das Verzeichnis $activation_map_dir ist leer. Es gibt keine Dateien zum Veröffentlichen."
  fi
}


publish_metrics() {
    publish_model_metrics
    publish_model_fairness_metrics
}

publish_metrics 
publish_model_metrics_noise "report_ml.md" "test/test-plots-rauschen/"
publish_model_metrics_disortion "report_ml.md" "test/test-plots-verzerrung/"
publish_model_metrics_rotation "report_ml.md" "test/test-rotation/"
publish_activation_map
