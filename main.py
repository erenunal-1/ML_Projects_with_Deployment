from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel, Field

# FastAPI app initialization
app = FastAPI()

# Load the trained model and pipeline
pipeline, model = joblib.load('best_catboost_model_pipeline.pkl')

# Define the schema for input data
class MLModelSchema(BaseModel):
    Person_ID: int = Field(..., title="Unique identifier for the person", json_schema_extra={"example": 1})
    Gender: str = Field(..., title="Gender of the person", max_length=6, 
                        description="Allowed values: 'Male' or 'Female'",
                        json_schema_extra={"example": "Male", "enum": ["Male", "Female"]})
    Age: int = Field(..., title="Age of the person", ge=0, le=100, json_schema_extra={"example": 27})
    Occupation: str = Field(..., title="Occupation of the person",
                            description="Allowed values: 'Software Engineer', 'Doctor', "
                                        "'Sales Representative', 'Teacher', 'Nurse', 'Engineer', "
                                        "'Accountant', 'Scientist', 'Lawyer', 'Salesperson', 'Manager'",
                            json_schema_extra={"example": "Software Engineer",
                            "enum": ["Software Engineer", "Doctor", "Sales Representative", 
                                    "Teacher", "Nurse", "Engineer", "Accountant", 
                                    "Scientist", "Lawyer", "Salesperson", "Manager"]})
    Sleep_Duration: float = Field(..., title="Duration of sleep in hours", gt=0, le=10, 
                                  description="Must be a positive number less than or equal to 10",
                                  json_schema_extra={"example": 6.1})
    Quality_of_Sleep: float = Field(..., title="Quality of sleep on a scale of 0-10", ge=0, le=10,
                                    description="Must be a number between 0 and 10 (inclusive)",
                                    json_schema_extra={"example": 6})
    Physical_Activity_Level: float = Field(..., title="Physical activity level on a scale of 0-10", ge=0, le=100, 
                                           description="Must be a number between 0 and 100 (inclusive)",
                                           json_schema_extra={"example": 42})
    Stress_Level: float = Field(..., title="Stress level on a scale of 0-10", ge=0, le=10,
                                description="Must be a number between 0 and 10 (inclusive)",
                                json_schema_extra={"example": 6})
    BMI_Category: str = Field(..., title="BMI category of the person", max_length=10,
                              description="Allowed values : 'Overweight', 'Normal' , 'Obese'",
                              json_schema_extra={"example": "Overweight",
                              "enum": ["Overweight", "Normal", "Obese"]})
    Blood_Pressure: str = Field(..., title="Blood pressure category",
                                description="Format: 'systolic/diastolic', e.g., '120/80'",
                                json_schema_extra={"example": '126/83'})
    Heart_Rate: float = Field(..., title="Heart rate in beats per minute", gt=0, le=100,
                              description="Must be a positive number less than or equal to 100",
                              json_schema_extra={"example": 77})
    Daily_Steps: int = Field(..., title="Number of daily steps", ge=0, le=20000,
                             description="Must be an integer between 0 and 20000 (inclusive)",
                             json_schema_extra={"example": 4200})
    

# Define preprocessing functions
def split_blood_pressure(df: pd.DataFrame) -> pd.DataFrame:
    df[["BP_Systolic", "BP_Diastolic"]] = df["Blood_Pressure"].str.split('/', expand=True)
    df[["BP_Systolic", "BP_Diastolic"]] = df[["BP_Systolic", "BP_Diastolic"]].apply(pd.to_numeric)
    df.drop("Blood_Pressure", axis=1, inplace=True)
    return df

def calculate_sleep_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df["Sleep_Efficiency"] = df["Sleep_Duration"] / df["Quality_of_Sleep"]
    df["Stress_Impact"] = df["Stress_Level"] / df["Quality_of_Sleep"]
    return df

def add_exercise_intensity(df: pd.DataFrame) -> pd.DataFrame:
    df['Exercise_Intensity'] = df['Physical_Activity_Level'].apply(
        lambda minutes: 'Low' if minutes <= 45 else
                        'Middle' if 45 < minutes <= 60 else
                        'Middle High' if 60 < minutes <= 75 else
                        'High'
    )
    return df

def segment_age(df: pd.DataFrame) -> pd.DataFrame:
    bins = [26, 35, 43, 50, 60]
    labels = ['Young', 'Middle-aged', 'Old', 'Very Old']
    df['Age_Segment'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    return df

@app.get("/")
def home():
    return {"message": "Welcome to the ML Model API!"}

@app.post("/predict")
def predict(data: MLModelSchema):

    # Convert input data to DataFrame
    input_data = pd.DataFrame([data.model_dump()])

    # Preprocess the input data
    input_data = split_blood_pressure(input_data)
    input_data = calculate_sleep_metrics(input_data)
    input_data = add_exercise_intensity(input_data)
    input_data = segment_age(input_data)

    # Drop the Person_ID column as it is not used for prediction
    input_data.drop(["Person_ID"], axis=1, inplace=True)

    # Apply the preprocessing pipeline to the input data
    processed_input_data = pipeline.transform(input_data)

    # Make prediction
    prediction = model.predict(processed_input_data)

    # Map prediction to sleep disorder
    sleep_disorder_map = {0: "None Sleep", 1: "Sleep Apnea", 2: "Insomnia"}
    prediction_label = sleep_disorder_map[int(prediction.item(0))]

    return {"prediction": prediction_label}
