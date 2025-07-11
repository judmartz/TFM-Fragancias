import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import joblib

# Datos (puedes cambiar esto a tu dataset real más adelante)
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run():
    # Parámetros
    max_depth = 4
    n_estimators = 80
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("n_estimators", n_estimators)

    # Entrenamiento
    model = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators)
    model.fit(X_train, y_train)

    # Evaluación
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)

    # Guarda el modelo localmente (DVC lo rastreará)
    os.makedirs("models", exist_ok=True)
    model_path = "models/model.joblib"
    joblib.dump(model, model_path)
    mlflow.log_artifact(model_path)
