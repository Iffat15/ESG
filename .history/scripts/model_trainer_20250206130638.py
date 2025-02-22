import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

def train_model(input_file='../data/energy_data.csv', output_file='../models/energy_model.pkl'):
    """
    Train a regression model to predict energy consumption.
    """
    df = pd.read_csv(input_file)
    X = df[['cpu_usage', 'memory_usage', 'disk_usage']]
    y = df['total_power']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    joblib.dump(model, output_file)
    print(f"Model trained and saved to {output_file}")

if __name__ == "__main__":
    train_model()
