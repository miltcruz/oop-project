# 🧠 Customer Churn Predictor (Docker + FastAPI)

This is my first full MLOps project where I took a machine learning model, wrapped it in a FastAPI app, and deployed it in a Docker container. If you’re new to this stuff — it means I trained a model to guess if a customer is about to leave, then built a little API around it that anyone can run and test.

---

## 🔧 What’s Inside

- 🧪 Trained a Scikit-learn model to predict churn  
- 🛠️ FastAPI app that loads the model and handles predictions  
- 🐳 Dockerfile so the whole thing can run in a container  
- 📦 requirements.txt for dependencies  
- 📊 Notebooks for EDA, training, and MLflow logging  

---

## How to Run
- Run ```bash pip install -r requirements.txt```
- cd scripts/
- Run ```bash python load_customer_data.py ```

## Build the container
- cd ..
- Open docker desktop
- Run ```bash docker build -t churn-api .```

## Run the app
- Run ```bash docker run -p 8000:8000 churn-api```

## Now open your browser to:
- Go to: http://localhost:8000/docs

You'll see the Swagger UI where you can test the /predict endpoint.

## 🔍 Sample Input for /predict
Here’s what to send in as JSON:

```json
{
    "CustomerID": 690279,
    "Gender": "Female",
    "Age": 43,
    "Tenure": 6,
    "Balance": 91462.89,
    "NumOfProducts": 2,
    "IsActiveMember": 1,
    "EstimatedSalary": 124101.3,
    "Exited": true,
    "MailingAddress": null,
    "BillingAddress": null
}
```

## It’ll respond with something like:

```json
{
  "churn_prediction": 1
}
```

## 📦 Files & Folders
Path	Purpose
api/	FastAPI app code
model/	Serialized .pkl model
notebooks/	EDA + training + tracking
Dockerfile	Build config for the container
requirements.txt	All the Python dependencies
data/   Local db and csv files
scripts/  Scripts needed to load db
microservices/  Various services used in the app
.env  App variables needed to run

🚀 Why I Built This
Curious about MLOps and wanted to actually build something I could test, run in Docker, and eventually deploy. This repo is part of my portfolio I am trying to build while in school.