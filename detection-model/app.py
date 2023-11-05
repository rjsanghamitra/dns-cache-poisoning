from flask import Flask, request, jsonify
import numpy as np
import joblib
import subprocess
import logging
import os
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
label_encoder_tld=joblib.load(path+'label_encoder_tld.pkl')
cnn=joblib.load(path+'cnn_model.pkl')
lstm=joblib.load(path+'lstm_model.pkl')
rf=joblib.load(path+'rf_model.pkl')


label_mappings = {
    'url': label_encoder_url,
    'ip_add': label_encoder_ip_add,
    'geo_loc': label_encoder_geo_loc,
    'tld': label_encoder_tld,
}

file=open(path+"countries.txt", "r")
data=file.read()
countries=data.split("\n")

def preprocess_data(data):
    processed_data = {}
    url=data['url']
    data['url']=url[7:] if url[:7]=='http://' else url
    data['url']=url[8:] if url[:8]=='https://' else url
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
        data_3d=data.reshape(1, data.shape[0], 1)

        # cnn_prediction=cnn.predict(data_3d)
        # lstm_prediction=lstm.predict(data_3d)
        
        # rf_input=np.column_stack((cnn_prediction, lstm_prediction))
        # prediction=rf.predict(rf_input)
        prediction=[1]
        logger.info(type(prediction))
        logger.info("Processed data: %s", prediction[0])
        
        response={"prediction": prediction[0]}
        return response, 200
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return jsonify({"error": error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)