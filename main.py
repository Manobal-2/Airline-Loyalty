
import pandas as pd
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report
import joblib

loyalty = pd.read_csv('data/Customer Loyalty History.csv')
activity = pd.read_csv('data/Customer Flight Activity.csv')

activity['Date'] = pd.to_datetime(activity['Year'].astype(str) + '-' + activity['Month'].astype(str) + '-01')

agg = activity.groupby('Loyalty Number').agg({
    'Total Flights':'sum',
    'Distance':'sum',
    'Points Accumulated':'sum',
    'Points Redeemed':'sum'
}).reset_index()

data = loyalty.merge(agg,on='Loyalty Number',how='left')

data['churn'] = data['Cancellation Year'].notna().astype(int)

features = [
    'CLV',
    'Salary',
    'Total Flights',
    'Distance',
    'Points Accumulated',
    'Points Redeemed'
]

data = data[features + ['churn']].fillna(0)

X = data[features]
y = data['churn']

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y
)

model = LGBMClassifier()
model.fit(X_train,y_train)

preds = model.predict(X_test)

print(classification_report(y_test,preds))

joblib.dump(model,'model.pkl')
