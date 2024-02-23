import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Assuming the data is loaded into a DataFrame df
df = pd.read_csv('data\FeedingDashboardData.csv')

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
df.iloc[:, 1:-1] = imputer.fit_transform(df.iloc[:, 1:-1])  # Exclude 'encounterId' and 'referral'

scaler = StandardScaler()
df.iloc[:, 1:-1] = scaler.fit_transform(df.iloc[:, 1:-1])  # Exclude 'encounterId' and 'referral'

X = df.drop(['encounterId', 'referral'], axis=1)
y = df['referral']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

svc = SVC(kernel='rbf', probability=True, random_state=42) 
svc.fit(X_train, y_train)

# Predict the probabilities of referral for the patients in the test set
probabilities = svc.predict_proba(X_test)[:, 1]  # The second column contains the probability estimates

# Print the referral probabilities for each patient
for i, prob in enumerate(probabilities):
    print(f"Patient {i+1} referral probability: {prob:.2f}")

# Assuming a threshold of 0.5
threshold = 0.5
referral_needed = probabilities > threshold

for i, need_referral in enumerate(referral_needed):
    print(f"Patient {i+1} needs referral: {'Yes' if need_referral else 'No'}")
