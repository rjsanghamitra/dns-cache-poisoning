print("Importing Packages")
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.ensemble import IsolationForest
import joblib
import os

cwd=os.getcwd()
print("Reading Dataset")
df=pd.read_csv(cwd+'/detection-model/Webpages_Dataset_Final.csv')
countries=df['geo_loc'].unique()

print("Exporting Countries List externally")
file=open(cwd+"/detection-model/countries.txt", "w")
for country in countries:
    file.write(country+"\n")
file.close()

df = df.loc[:, ~df.columns.str.match('Unnamed: ')]
df=df.drop(['who_is','js_len','js_obf_len','content'], axis=1)
print("Columns Dropped")

print("Finding Categorical Columns")
numerical_vars = df.columns[df.dtypes != "object"]
categorical_vars = df.columns[df.dtypes == "object"]

# print(numerical_vars)
# print(categorical_vars)

print("Creating Label Encoder pkl files")
le = LabelEncoder()
for label in categorical_vars:
    df[label] = le.fit_transform(df[label])
    joblib.dump(le, cwd+'/detection-model/label_encoder_'+label+'.pkl')
print("Created Label Encoder pkl files")

print("Initialising dependent and independent variables")
x = df.drop('label', axis=1)
y = df["label"]


print("Intialising Standard Scaler")
scaler = StandardScaler()
x=scaler.fit_transform(x)

print("Building Isolation Forest Model")
iso_forest = IsolationForest(contamination=0.05)
iso_forest.fit(x)
iso_scores=iso_forest.decision_function(x)

print("Updating Dataset with ISO Scores")
df['iso']=iso_scores

x=scaler.fit_transform(x)

print("Building Linear SVM Model")
svm=LinearSVC(random_state=42)
svm.fit(x, y)

print("Creating ISO Forest pkl")
joblib.dump(iso_forest, cwd+'/detection-model/iso_forest_model.pkl')
print("Created ISO Forest pkl")

print("Creating Linear SVM pkl")
joblib.dump(svm, cwd+'/detection-model/linear_svm_model.pkl')
print("Created Linear SVM pkl")

print("Done")