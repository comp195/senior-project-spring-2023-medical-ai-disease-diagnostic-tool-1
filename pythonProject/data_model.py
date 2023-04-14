# Libraries we need for this project

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the preprocessed data and selected features from the CSV files
processed_data = pd.read_csv('processed_data.csv')
corr_features = pd.read_csv('corr_features.csv', header=None).iloc[:, 0].tolist()
chi2_features = pd.read_csv('chi2_features.csv', header=None).iloc[:, 0].tolist()
rfe_features = pd.read_csv('rfe_features.csv', header=None).iloc[:, 0].tolist()

# Create a dictionary containing the names and lists of different feature sets
feature_sets = {
    'all_features': processed_data.drop('HeartDisease', axis=1).columns.tolist(),  # All features in the dataset
    'corr_features': corr_features,  # Top 10 features based on correlation
    'chi_features': chi2_features,  # Top 10 features based on Chi-squared test
    'rfe_features': rfe_features,  # Top 10 features based on Recursive Feature Elimination
}
print(feature_sets)

# Iterate through the feature sets
for name, features in feature_sets.items():
    X = processed_data[features]  # Choose the features that belong to the current set of features.
    y = processed_data['HeartDisease']  # Set the term 'HeartDisease' as the goal.

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()  # Put the logistic regression model into action
    model.fit(X_train, y_train)  # Use the training data to fit the model.

    y_pred = model.predict(X_test)  # Make predictions based on the test results
    accuracy = accuracy_score(y_test, y_pred)  # Figure out how accurate the model's predictions are.

    print(f"Accuracy for {name}: {accuracy}")  # Print the accuracy for the current feature set

