# === 🌐 FastAPI Churn Prediction Service ===
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Depends, HTTPException
import joblib
import numpy as np
from microservices.customer_service.customer_service import CustomerService
from microservices.customer_service.entities.customer import Customer
from microservices.data_acccess_service.repositories.customer_repository import CustomerRepository
from microservices.data_acccess_service.providers.sqlite_provider import SqliteProvider
from microservices.data_acccess_service.providers.sqlserver_provider import SqlServerProvider

""" For some reason I have to put uvicorn api.main:app --reload
in the terminal to run this file, even though I have the FastAPI extension installed in VSCode."""

# loads variables from .env
load_dotenv()

# 🚀 Start FastAPI app
app = FastAPI(title="Customer Churn Predictor")

# OOP Examples Customer Service
def get_customer_service() -> CustomerService:
    provider_name = os.getenv("DB_PROVIDER").lower()

    if provider_name == "sqlserver":
        conn_str = os.getenv("SQLSERVER_URL")  # full pyodbc string
        provider = SqlServerProvider(conn_str)
    else:
        db_path = os.path.abspath(os.getenv("SQLITE_DB_PATH"))
        provider = SqliteProvider(db_path)

    repo = CustomerRepository(provider)
    return CustomerService(repo)


@app.get("/customers")
def list_customers(svc: CustomerService = Depends(get_customer_service)):
    return list(svc.list_customers(limit=10))

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int, svc: CustomerService = Depends(get_customer_service)):
    c = svc.get_customer(customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c



# 🔄 Load the trained model (make sure path is correct)
model = joblib.load("./model/churn_model.pkl")

# 🏠 Root route
@app.get("/")
def read_root():
    return {"message": "🔥 Churn Prediction API is live!"}

# 🔮 Prediction route
@app.post("/predict")
def predict_churn(data: Customer):
    # Turn incoming data into the format the model expects
    input_array = np.array([[
        data.Gender,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.IsActiveMember,
        data.EstimatedSalary
    ]])
    
    # Run prediction
    prediction = model.predict(input_array)[0]
    label = "Will Churn" if prediction == 1 else "Will Stay"
    
    return {
        "prediction": int(prediction),
        "label": label
    }