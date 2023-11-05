from flask import Flask, request, jsonify
import os
import numpy as np
import joblib
import logging
import random

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

app=Flask(__name__)

cwd=os.getcwd()
path=cwd+"/detection_model/jobfiles/"
label_encoder_url=joblib.load(path+"label_encoder_url.pkl")
label_encoder_ip_add=joblib.load(path+"label_encoder_ip_add.pkl")
label_encoder_tld=joblib.load(path+"label_encoder_tld.pkl")
label_encoder_https=joblib.load(path+"label_encoder_https.pkl")
label_encoder_geo_loc=joblib.load(path+"label_encoder_geo_loc.pkl")
cnn_model=joblib.load(path+"cnn_model.pkl")
lstm_model=joblib.load(path+"lstm_model.pkl")
rf_model=joblib.load(path+"rf_model.pkl")

label_map={
    'url': label_encoder_url,
    'ip_add': label_encoder_ip_add,
    'tld': label_encoder_tld,
    'is_https': label_encoder_https,
    'geo_loc': label_encoder_geo_loc
}

file=open(cwd+"/detection_model/countries.txt", "r")
data=file.read()
countries=data.split("\n")
file.close()

file1=open(cwd+"/attack/list.txt", "r")
data=file1.read()
ips1=data.split("\n")
file1.close()

def preprocess_data(data):
    processed_data={}
    for column, label_encoder in label_map.items():
        # print(column)
        try:
            label=label_encoder.transform([data[column]])[0]
            processed_data[column]=label
            # print(type(label))
        except Exception as e:
            # logger.warning(e)
            processed_data[column]=-1
    # print("Loop Complete")
    return processed_data

@app.route('/predict', methods=['POST'])
def funcPredictions():
    try:
        req_data=request.get_json()
        if req_data["ip_add"] in ips1:
            logger.info("Prediction: %s", 0)
            response={"prediction": "0"}
            return response, 200
        # logger.info("%s", req_data)
        req_data['geo_loc']=countries[random.randint(0, len(countries)-1)]
        # logger.info("%s", req_data)
        data=list(preprocess_data(req_data).values())
        # logger.info("%s", data)
        data.insert(2, req_data['url_len'])
        # logger.info("%s", data)
        data.insert(0, 0)
        data=np.array(data)
        data_3d=data.reshape(1, data.shape[0], 1)        
        # logger.info("%s", data)


        cnn_prediction=cnn_model.predict(data_3d)
        # logger.info("%s", data)

        lstm_prediction=lstm_model.predict(data_3d)

        rf_input=np.column_stack((cnn_prediction, lstm_prediction))
        prediction=rf_model.predict(rf_input)
        # logger.info("%s", data)

        logger.info("Prediction: %s", prediction[0])
        response={"prediction": f"{prediction[0]}"}
        # logger.info(response)
        return response, 200
    except Exception as e:
        error_message=f"Error: {str(e)}"
        return jsonify({"error": error_message}), 400
    
if __name__ == "__main__":
    app.run(debug=True)