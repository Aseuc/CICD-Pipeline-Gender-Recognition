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

publish_metrics() {
    local report_file=$1
    publish_model_metrics
    publish_model_fairness_metrics
    cml-send-comment "$report_file"

}




publish_metrics "report_ml.md"