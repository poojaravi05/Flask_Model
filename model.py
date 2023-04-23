import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Load the dataset
df = pd.read_csv('toy_car_data.csv')

# Extract input features (X) and target variable (y)
X = df[['Year', 'Mileage']].values
y = df['Price (USD)'].values

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train, y_train)

# Save the model to a file using pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Load the saved model from file
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Evaluate the model on the test data
y_pred = model.predict(X_test)
