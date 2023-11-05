print("Importing Packages")
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, LSTM
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("Reading Dataset")
cwd=os.getcwd()
df=pd.read_csv(cwd+'/dataset/Webpages_Classification_train_data.csv')

# countries=df['geo_loc'].unique()
# file=open(path+"countries.txt", "w")
# for country in countries:
#     file.write(country+"\n")
# file.close()

print("Finding Categorical Columns for Label Encoding")
numerical_vars = df.columns[df.dtypes != "object"]
categorical_vars = df.columns[df.dtypes == "object"]

# print(numerical_vars)
# print(categorical_vars)

print("Label Encoder")
le = LabelEncoder()
for label in categorical_vars:
    df[label] = le.fit_transform(df[label])
    joblib.dump(le, cwd+'label_encoder_'+label+'.pkl')

x = df.drop('label', axis=1)
y = df["label"]

print("Scaling")
scaler = StandardScaler()
x=scaler.fit_transform(x)

print("Splitting")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
print(len(x_train))

# print("CNN")
num_rows, num_columns = x_train.shape
x_train_3d = x_train.reshape(num_rows, num_columns, 1)
# # # import keras
# cnn_model = Sequential()
# cnn_model.add(Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(x_train_3d.shape[1], x_train_3d.shape[2])))
# cnn_model.add(MaxPooling1D(pool_size=2))
# cnn_model.add(Flatten())
# cnn_model.add(Dense(64, activation='relu'))
# cnn_model.add(Dense(1, activation='sigmoid'))

# cnn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# cnn_model.fit(x_train_3d, y_train, epochs=10, batch_size=32)
# num_rows_test, num_columns_test = x_test.shape
# x_test_3d = x_test.reshape(num_rows_test, num_columns_test, 1)


print("CNN Accuracy")
# loss, accuracy = cnn_model.evaluate(x_test_3d, y_test)
# print("Test loss: "+loss+", Test accuracy: "+accuracy)


print("LSTM")
lstm_model = Sequential()
lstm_model.add(LSTM(64, activation='relu', input_shape=(x_train_3d.shape[1], x_train_3d.shape[2])))
lstm_model.add(Dense(1, activation='sigmoid'))
lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', 'mse'])
lstm_model.fit(x_train_3d, y_train, epochs=10, batch_size=32)
# Evaluate the model

print("LSTM Accuracy")
# loss, accuracy = lstm_model.evaluate(x_test_3d, y_test)
# print("Test loss: "+loss+", Test accuracy: "+accuracy)

# cnn_predictions = cnn_model.predict(x_train_3d)
# lstm_predictions = lstm_model.predict(x_train_3d)


# print("Random Forest")
# # Combine the predictions as features for the Random Forest
# ensemble_features = np.column_stack((cnn_predictions, lstm_predictions))
# # Split the data into training and testing sets for the Random Forest
# x_train_rf, x_test_rf, y_train_rf, y_test_rf = train_test_split(ensemble_features, y_test, test_size=0.2, random_state=42)

# # Train the Random Forest classifier
# rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
# rf_classifier.fit(x_train_rf, y_train_rf)

# # Make predictions using the Random Forest ensemble
# ensemble_predictions = rf_classifier.predict(x_test_rf)

# # Calculate the accuracy of the ensemble
# accuracy = accuracy_score(y_test_rf, ensemble_predictions)
# print("Ensemble Accuracy: {accuracy}")


# print("Joblib")
# joblib.dump(cnn_model, path+'cnn_model.pkl')
# joblib.dump(lstm_model, path+'lstm_model.pkl')
# joblib.dump(rf_classifier, path+'rf_model.pkl')


