import os
from argparse import ArgumentParser
import mlflow
import pandas as pd
import psycopg2
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from preprocessing import preprocess_input


os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"


def load_dataset_from_db():
    db_connect = psycopg2.connect(
        user="pguser",
        password="pgpassword",
        host="localhost",
        port=5432,
        database="pgdatabase",
    )
    df = pd.read_sql("SELECT * FROM loan_data", db_connect)
    db_connect.close()
    return df


def dataset_pipeline():
    df = load_dataset_from_db() 
    preprocess_input(df)
    return df

def model_train_and_log(df):

    train = df[~df["대출등급"].isnull()]
    X = train.drop(["id", "timestamp", "대출등급"], axis=1)
    y = train["대출등급"]

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, 
                                                          test_size=0.2, 
                                                          random_state=2025)

    params = {
        "n_estimators": 1000,
        "max_depth": 16,
        "num_leaves": 40,
        "min_child_samples": 11,
        "min_child_weight": 4,
        "learning_rate": 0.0348,
        "subsample": 0.8888,
        "colsample_bytree": 0.3714,
        "reg_alpha": 2.5,
        "reg_lambda": 7.08,
    }
    model = LGBMClassifier(**params)
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    valid_pred = model.predict(X_valid)

    train_acc = accuracy_score(y_train, train_pred)
    valid_acc = accuracy_score(y_valid, valid_pred)

    print(f"Train Accuracy: {train_acc:.4f}")
    print(f"Valid Accuracy: {valid_acc:.4f}")


    parser = ArgumentParser()
    parser.add_argument("--model-name", dest="model_name", type=str, default="lgbm_model")
    args = parser.parse_args()


    mlflow.set_experiment("new-exp")
    signature = mlflow.models.signature.infer_signature(model_input=X_train, model_output=train_pred)
    input_sample = X_train.iloc[:10]

    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metrics({"train_acc": train_acc, "valid_acc": valid_acc})
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=args.model_name,
            signature=signature,
            input_example=input_sample,
        )

    return model


if __name__=="__main__":
    df = dataset_pipeline()
    model_train_and_log(df)