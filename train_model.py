import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_extract
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator


# -----------------------------
# Spark session
# -----------------------------
spark = (
    SparkSession.builder
    .appName("CreditRiskProject")
    .master("local[*]")
    .getOrCreate()
)

print("Spark Version:", spark.version)


# -----------------------------
# Load dataset
# -----------------------------
df = spark.read.csv(
    "/app/credit_risk_small.csv",
    header=True,
    inferSchema=False
)

print("Data loaded successfully")
print("Total columns:", len(df.columns))


# -----------------------------
# Select useful columns
# -----------------------------
selected_cols = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "emp_length",
    "home_ownership",
    "annual_inc",
    "verification_status",
    "loan_status",
    "purpose",
    "dti",
    "delinq_2yrs",
    "fico_range_low",
    "fico_range_high",
    "inq_last_6mths",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "total_acc"
]

df_selected = df.select(selected_cols)

# Keep only completed loan outcomes
df_final = df_selected.filter(
    col("loan_status").isin(["Fully Paid", "Charged Off"])
)

print("Final loan records:", df_final.count())


# -----------------------------
# Create target variable
# -----------------------------
df_target = df_final.withColumn(
    "default_flag",
    when(col("loan_status") == "Charged Off", 1)
    .otherwise(0)
)


# -----------------------------
# Convert numeric columns
# -----------------------------
numeric_cols = [
    "loan_amnt",
    "int_rate",
    "installment",
    "annual_inc",
    "dti",
    "delinq_2yrs",
    "fico_range_low",
    "fico_range_high",
    "inq_last_6mths",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "total_acc"
]

df_numeric = df_target

for column_name in numeric_cols:
    df_numeric = df_numeric.withColumn(
        column_name,
        col(column_name).cast("double")
    )


# -----------------------------
# Fill missing values
# -----------------------------
df_clean = df_numeric.fillna({
    "dti": 18.37,
    "revol_util": 50.5,
    "emp_length": "Unknown"
})


# -----------------------------
# Feature engineering
# -----------------------------
df_features = (
    df_clean
    .withColumn(
        "fico_avg",
        (col("fico_range_low") + col("fico_range_high")) / 2
    )
    .withColumn(
        "term_months",
        regexp_extract(
            col("term"),
            r"(\d+)",
            1
        ).cast("double")
    )
)


# -----------------------------
# Features
# -----------------------------
numeric_features = [
    "loan_amnt",
    "term_months",
    "int_rate",
    "annual_inc",
    "dti",
    "fico_avg"
]

categorical_features = [
    "grade",
    "emp_length",
    "home_ownership",
    "verification_status",
    "purpose"
]

indexers = [
    StringIndexer(
        inputCol=feature,
        outputCol=feature + "_index",
        handleInvalid="keep"
    )
    for feature in categorical_features
]

encoder = OneHotEncoder(
    inputCols=[
        feature + "_index"
        for feature in categorical_features
    ],
    outputCols=[
        feature + "_vec"
        for feature in categorical_features
    ]
)

assembler = VectorAssembler(
    inputCols=(
        numeric_features
        + [
            feature + "_vec"
            for feature in categorical_features
        ]
    ),
    outputCol="features",
    handleInvalid="keep"
)


# -----------------------------
# Train-test split
# -----------------------------
train_df, test_df = df_features.randomSplit(
    [0.8, 0.2],
    seed=42
)

print("Train rows:", train_df.count())
print("Test rows:", test_df.count())


# -----------------------------
# Weighted Logistic Regression
# -----------------------------
train_weighted = train_df.withColumn(
    "class_weight",
    when(col("default_flag") == 1, 3.8846047540077393)
    .otherwise(1.0)
)

lr_weighted = LogisticRegression(
    featuresCol="features",
    labelCol="default_flag",
    weightCol="class_weight",
    predictionCol="prediction",
    probabilityCol="probability",
    rawPredictionCol="rawPrediction",
    maxIter=50,
    regParam=0.01,
    elasticNetParam=0.0
)

weighted_pipeline = Pipeline(
    stages=indexers + [
        encoder,
        assembler,
        lr_weighted
    ]
)


# -----------------------------
# Train model
# -----------------------------
weighted_model = weighted_pipeline.fit(train_weighted)

print("Weighted Logistic Regression trained successfully")


# -----------------------------
# Evaluate model
# -----------------------------
weighted_predictions = weighted_model.transform(test_df)

roc_evaluator = BinaryClassificationEvaluator(
    labelCol="default_flag",
    rawPredictionCol="rawPrediction",
    metricName="areaUnderROC"
)

pr_evaluator = BinaryClassificationEvaluator(
    labelCol="default_flag",
    rawPredictionCol="rawPrediction",
    metricName="areaUnderPR"
)

roc_auc = roc_evaluator.evaluate(weighted_predictions)
pr_auc = pr_evaluator.evaluate(weighted_predictions)

print("Weighted ROC-AUC:", roc_auc)
print("Weighted PR-AUC:", pr_auc)


# -----------------------------
# Save model
# -----------------------------
model_path = "/app/model/credit_risk_model"

os.makedirs("/app/model", exist_ok=True)

weighted_model.write().overwrite().save(model_path)

print("Model saved successfully at:", model_path)

spark.stop()