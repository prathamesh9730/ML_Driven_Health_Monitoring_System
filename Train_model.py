import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("health_data.csv")  # your CSV file with labeled data

X = df.drop("status", axis=1)   # features
y = df["status"]                # labels (Normal, Warning, Critical)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("✅ Model trained and saved as  model.pkl")
