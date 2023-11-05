# For setting good to 1, bad to 0 in the dataset in the labels column

import pandas as pd
import os

cwd=os.getcwd()
path=cwd+'/dataset/'

dataset=path+'Webpages_Classification_train_data.csv'

print("Reading Database")
df=pd.read_csv(dataset)

print("Working on Database")
df['label']=df['label'].map(lambda x: 1 if x=='good' else 0)

# df['url']=df['url'].map(lambda x: x[7:] if x[:7]=='http://' else x)
# df['url']=df['url'].map(lambda x: x[8:] if x[:8]=='https://' else x)
df.to_csv(dataset, index=False)
