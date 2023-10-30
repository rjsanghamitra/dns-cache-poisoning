from flask import Flask, request, jsonify
import numpy as np
import joblib
import subprocess
import logging

logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

# Create a logger
logger = logging.getLogger(__name__)

app = Flask(__name__)

# script_path = 'detection-model\\detect.py'
# try:
#     subprocess.run(['python', script_path], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# except subprocess.CalledProcessError as e:
#     print(f"An error occurred: {e.stderr}")

label_encoder_url=joblib.load('detection-model\\label_encoder_url.pkl')
label_encoder_ip_add=joblib.load('detection-model\\label_encoder_ip_add.pkl')
label_encoder_geo_loc=joblib.load('detection-model\\label_encoder_geo_loc.pkl')
label_encoder_https=joblib.load('detection-model\\label_encoder_https.pkl')
label_encoder_tld=joblib.load('detection-model\\label_encoder_tld.pkl')
label_encoder_who_is=joblib.load('detection-model\\label_encoder_who_is.pkl')
iso=joblib.load('detection-model\\iso_forest_model.pkl')
svm=joblib.load('detection-model\\linear_svm_model.pkl')


label_mappings = {
    'url': label_encoder_url,
    'ip_add': label_encoder_ip_add,
    'geo_loc': label_encoder_geo_loc,
    'https': label_encoder_https,
    'who_is': label_encoder_who_is,
    'tld': label_encoder_tld,
}

def preprocess_data(data):
    processed_data = {}

    for column, label_encoder in label_mappings.items():
        try:
            label = label_encoder.transform([data[column]])[0]
            processed_data[column] = label
        except ValueError:
            processed_data[column]=-1
            
    return processed_data

@app.route('/predict', methods=['POST'])
def funcPredictions():
    try:
        req_data=request.json
        
        data=list(preprocess_data(req_data).values())
        data.insert(1, req_data['url_len'])
        data.insert(7, req_data['js_len'])
        data.insert(8, req_data['js_obf_len'])
        data=np.array(data)
        
        iso_prediction=iso.predict([data])
        
        data=data+iso_prediction
        prediction = svm.predict([data])
        logger.info("Processed data: %s", prediction[0])
        
        

        response = {"": f"{prediction[0]}"}
        return jsonify(response), 200
    except Exception as e:
        # Handle errors and return an error response
        error_message = f"Error: {str(e)}"
        return jsonify({"error": error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)