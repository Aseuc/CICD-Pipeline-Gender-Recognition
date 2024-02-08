publish_model_metrics() {
    echo "## Model Metriken" > report_ml.md
    cat test/metrics/metrics.txt >> report_ml.md
    echo 'cml-publish   test/metrics/metrics.jpg --md >> report_ml.md' > publish_metrics.sh
}


publish_model_fairness_metrics(){
    echo "\n## Fairlearn Ergebnisse" >> report_ml.md
    echo 'cml-publish test/metricsFairlearn/Fig1metricsFairLearn.jpg --md >> report_ml.md' >> publish_metrics.sh
    echo 'cml-publish test/metricsFairlearn/Fig2metricsFairLearn.jpg --md >> report_ml.md' >> publish_metrics.sh

}

publish_model_metrics_noise(){
            local report_file=$1
            local noise_plot_data_dir=$2
            echo "## Modellmetriken mit verauschten Bilder" > $report_file      
            for file in $noise_plot_data_dir/*.png; do
                echo "Veröffentlichung $file"
                cml-publish "$file" --md >> $report_file
            done
            cml-send-comment $report_file
            
}
publish_model_metrics_disortion(){
    local report_file=$1
    local distortion_plot_data_dir=$2
    echo "## Modellmetriken mit verzerrten Bildern" > $report_file      
    for file in $distortion_plot_data_dir/*.png; do
        echo "Veröffentlichung $file"
        cml-publish "$file" --md >> $report_file
    done
    cml-send-comment $report_file
            
}

publish_model_metrics_rotation(){
    local report_file=$1
    local rotation_plot_data_dir=$2
    echo "## Modellmetriken mit verdrehte Bilder" > $report_file      
    for file in $rotation_plot_data_dir/*.png; do
        echo "Publishing $file"
        cml-publish "$file" --md >> $report_file
    done
    cml-send-comment $report_file
}

           

publish_metrics() {
    local report_file=$1
    publish_model_metrics
    publish_model_fairness_metrics
    cml-send-comment "$report_file"

}


publish_metrics "report_ml.md" 
publish_model_metrics_noise "report_test_rauschen.md" "test/test-plots-rauschen"
publish_model_metrics_disortion "report_test_verzerrung.md" "test/test-plots-verzerrung"
publish_model_metrics_rotation "report_rotation.md" "test/test-plots-rotation"