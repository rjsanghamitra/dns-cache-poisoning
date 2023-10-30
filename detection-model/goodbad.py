# For setting good to 1, bad to 0 in the dataset in the labels column

import pandas as pd
dataset='detection-model\\Webpages_Classification_test_data.csv'

df=pd.read_csv(dataset)
df['label']=df['label'].map(lambda x: 1 if x=='good' else 0)
df.to_csv(dataset, index=False)

