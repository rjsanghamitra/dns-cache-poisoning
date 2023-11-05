print("Importing Packages")
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, LSTM

print("Reading Dataset")
cwd=os.getcwd()
df=pd.read_csv(cwd+"/dataset/Webpages_Classification_train_data.csv")

countries=df['geo_loc'].unique()
file=open(cwd+"/detection_model/countries.txt", "w")
for country in countries:
    file.write(country+"\n")
file.close()

df.drop(["who_is", "js_len", "js_obf_len", "content"], axis=1, inplace=True)

print("Finding Numerical and Categorical Values")
numerical_vars=df.columns[df.dtypes!="object"]
categorical_vars=df.columns[df.dtypes=="object"]
print(numerical_vars)
print(categorical_vars)

print("Initiating Label Encoding")
for label in categorical_vars:
    le=LabelEncoder()
    df[label]=le.fit_transform(df[label])
    joblib.dump(le, cwd+"/detection_model/jobfiles/label_encoder_"+label+".pkl")

x=df.drop("label", axis=1)
y=df["label"]

print("Scaling Features")
scaler=StandardScaler()
x=scaler.fit_transform(x)

print("Reshaping Data for the model")
num_rows, num_columns=x.shape
x_3d=x.reshape(num_rows, num_columns, 1)

print("Building CNN Model")
cnn_model=Sequential()
cnn_model.add(Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(x_3d.shape[1], x_3d.shape[2])))
cnn_model.add(MaxPooling1D(pool_size=2))
cnn_model.add(Flatten())
cnn_model.add(Dense(64, activation='relu'))
cnn_model.add(Dense(1, activation='sigmoid'))

cnn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', 'mse'])
cnn_model.fit(x_3d, y, epochs=10, batch_size=32)

print("Building LSTM Model")
lstm_model=Sequential()
lstm_model.add(LSTM(64, activation='relu', input_shape=(x_3d.shape[1], x_3d.shape[2])))
lstm_model.add(Dense(1, activation='sigmoid'))

lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', 'mse'])
lstm_model.fit(x_3d, y, epochs=10, batch_size=32)

cnn_predictions=cnn_model.predict(x_3d)
lstm_prediction=lstm_model.predict(x_3d)

print("Building the Ensemble Random Forest Classifier")
ensemble_features=np.column_stack((cnn_predictions, lstm_prediction))

rf_model=RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(ensemble_features, y)

print("Exporting Models")
joblib.dump(cnn_model, cwd+"/detection_model/jobfiles/cnn_model.pkl")
joblib.dump(lstm_model, cwd+"/detection_model/jobfiles/lstm_model.pkl")
joblib.dump(rf_model, cwd+"/detection_model/jobfiles/rf_model.pkl")