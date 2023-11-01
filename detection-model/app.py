from flask import Flask, request, jsonify
import numpy as np
import joblib
import subprocess
import logging
import os
import json
import random

logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

# Create a logger
logger = logging.getLogger(__name__)

app = Flask(__name__)

# script_path = 'detection-model\\detect.py'
# try:
#     subprocess.run(['python', script_path], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# except subprocess.CalledProcessError as e:
#     print(f"An error occurred: {e.stderr}")

cwd=os.getcwd()
path=cwd+'/detection-model/'
label_encoder_url=joblib.load(path+'label_encoder_url.pkl')
label_encoder_ip_add=joblib.load(path+'label_encoder_ip_add.pkl')
label_encoder_geo_loc=joblib.load(path+'label_encoder_geo_loc.pkl')
label_encoder_https=joblib.load(path+'label_encoder_https.pkl')
label_encoder_tld=joblib.load(path+'label_encoder_tld.pkl')
iso=joblib.load(path+'iso_forest_model.pkl')
svm=joblib.load(path+'linear_svm_model.pkl')


label_mappings = {
    'url': label_encoder_url,
    'ip_add': label_encoder_ip_add,
    'geo_loc': label_encoder_geo_loc,
    'https': label_encoder_https,
    'tld': label_encoder_tld,
}

file=open(path+"countries.txt", "r")
data=file.read()
countries=data.split("\n")

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
        req_data=request.get_json()
        req_data['geo_loc']=countries[random.randint(0, len(countries)-1)]
        data=list(preprocess_data(req_data).values())
        data.insert(1, req_data['url_len'])
        logger.info("%s", data)
        data=np.array(data)
        
        iso_prediction=iso.predict([data])
        
        data=data+iso_prediction
        svm_prediction = svm.predict([data])
        prediction=svm_prediction.tolist()
        logger.info(type(prediction))
        logger.info("Processed data: %s", prediction[0])
        
        response={"prediction": prediction[0]}
        return response, 200
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return jsonify({"error": error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)