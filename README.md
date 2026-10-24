# ML Model Failure Prediction and Early Warning System

## 📌 Project Overview

The **ML Model Failure Prediction and Early Warning System** is a machine learning project designed to predict potential machine failures, detect changes in incoming data, and monitor prediction patterns.

The goal is to build a reusable ML pipeline that can generate early warnings, identify data drift, and help assess when a model may require further investigation.

## 🎯 Objectives

- Predict potential machine failures using machine learning.
- Detect data drift in incoming machine readings.
- Generate early warnings based on prediction thresholds.
- Evaluate model performance using classification metrics.
- Build reusable prediction and monitoring functions.
- Prepare the system for API-based deployment and production monitoring.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| scikit-learn | Model training, preprocessing, and evaluation |
| SciPy | Statistical drift detection |
| Joblib | Saving and loading trained models |
| Evidently | Planned data and model monitoring |
| FastAPI | Planned prediction API |
| PostgreSQL | Planned storage for predictions and monitoring records |
| Docker | Planned application containerization |
| Prometheus | Planned application metrics |
| Grafana | Planned monitoring dashboards |

## 📊 Dataset

This project uses the **AI4I 2020 Predictive Maintenance Dataset**.

The dataset contains 10,000 records with machine operating measurements and failure-related labels.

### Selected Features

- Type
- Air temperature [K]
- Process temperature [K]
- Rotational speed [rpm]
- Torque [Nm]
- Tool wear [min]

### Target Variable

`Machine failure`

- `0` — No machine failure recorded.
- `1` — Machine failure recorded.

The dataset is imbalanced, with substantially more normal records than failure records. Therefore, precision, recall, F1-score, and average precision are important evaluation metrics.

## 🧠 Machine Learning Approach

The current implementation uses a **Random Forest Classifier** to predict potential machine failures.

The workflow includes:

1. Dataset inspection and exploratory data analysis.
2. Feature selection and preprocessing.
3. Train/test splitting.
4. Model training.
5. Classification evaluation.
6. Decision-threshold experiments.
7. Simulated data drift detection.
8. Reusable prediction functions.
9. Model persistence and preparation for deployment.

## 📈 Model Evaluation

The model is evaluated using:

- Precision
- Recall
- F1-score
- Confusion matrix
- Average precision (PR-AUC)

Because machine failures are relatively rare, accuracy alone is not sufficient to assess model quality.

The classification threshold can be adjusted to explore the trade-off between detecting more failures and generating fewer false alarms.

## 🔍 Data Drift Detection

The project uses the **Kolmogorov–Smirnov (KS) test** to compare feature distributions between reference data and incoming data.

The monitoring workflow includes:

- Comparing reference and incoming feature distributions.
- Calculating KS statistics and p-values.
- Applying a multiple-testing correction.
- Flagging features whose distributions have changed significantly.
- Generating a monitoring summary.

A simulated torque shift is used to test the drift detection workflow.

**Important:** Data drift does not automatically mean that model performance has degraded. Actual performance assessment requires appropriate ground-truth labels.

## 🏗️ Project Structure

```text
ml-model-failure-warning/
│
├── configs/
│   └── Configuration files
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── Saved model artifacts
│
├── notebooks/
│   └── Exploratory analysis and experiments
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── monitoring/
│   └── api/
│
├── tests/
│   └── Automated tests
│
├── .gitignore
├── README.md
└── requirements.txt
```

*Note: This represents the planned project structure. Add directories and files as their components are implemented.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <your