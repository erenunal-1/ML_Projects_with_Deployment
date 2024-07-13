# End-to-End Machine Learning Project with Deployment

## Project Overview

The primary goal of this project is to develop, deploy, and manage a machine learning model for predicting sleep disorders using various health and lifestyle metrics. This project leverages FastAPI for API development, CatBoost for the machine learning model, and Google Cloud Run for deployment.

## Project Purpose

This project demonstrates the following objectives:

**CI/CD Integration:** Automates the process of testing and deploying machine learning models using GitHub Actions. 

**Efficient Model Deployment:** Ensures rapid and reliable deployment of models to production environments.

**Lifecycle Management:** Manages the entire lifecycle of the model, from training and evaluation to deployment and monitoring.

**Collaboration Enhancement:** Increases collaboration between development and operations teams through continuous integration and continuous deployment (CI/CD) practices.

**Reliability and Consistency:** Ensures that models maintain their expected performance through rigorous testing processes.

## Dataset

The dataset used in this project, **Sleep Health and Lifestyle Dataset**, contains 400 rows and 13 columns with various health and lifestyle metrics of individuals. This dataset includes:

- **Person ID**: An identifier for each individual.
- **Gender**: The gender of the person (Male/Female).
- **Age**: The age of the person in years.
- **Occupation**: The occupation or profession of the person.
- **Sleep Duration (hours)**: The number of hours the person sleeps per day.
- **Quality of Sleep (scale: 1-10)**: A subjective rating of the quality of sleep, ranging from 1 to 10.
- **Physical Activity Level (minutes/day)**: The number of minutes the person engages in physical activity daily.
- **Stress Level (scale: 1-10)**: A subjective rating of the stress level experienced by the person, ranging from 1 to 10.
- **BMI Category**: The BMI category of the person (e.g., Underweight, Normal, Overweight).
- **Blood Pressure (systolic/diastolic)**: The blood pressure measurement of the person, indicated as systolic pressure over diastolic pressure.
- **Heart Rate (bpm)**: The resting heart rate of the person in beats per minute.
- **Daily Steps**: The number of steps the person takes per day.
- **Sleep Disorder**: The presence or absence of a sleep disorder in the person (None, Insomnia, Sleep Apnea).

### Target Variable: Sleep Disorder
- **None**: The individual does not exhibit any specific sleep disorder.
- **Insomnia**: The individual experiences difficulty falling asleep or staying asleep, leading to inadequate or poor-quality sleep.
- **Sleep Apnea**: The individual suffers from pauses in breathing during sleep, resulting in disrupted sleep patterns and potential health risks.

*Note: The data presented is synthetic and created for illustrative purposes.*

## Model

The model employed for this project is a **CatBoost Classifier**. The data preprocessing and feature engineering steps include the following:

- **Splitting Blood Pressure**: The blood pressure values are split into systolic and diastolic components for more granular analysis.
- **Calculating Sleep Efficiency**: A new feature representing sleep efficiency is derived to enhance the understanding of sleep patterns.
- **Calculating Stress Impact**: A feature indicating the impact of stress on individuals' health metrics is computed.
- **Categorizing Exercise Intensity**: Physical activity levels are categorized into different intensity levels.
- **Segmenting Age**: Age is segmented into meaningful categories to capture demographic variations.

### Model Training
The **CatBoost** algorithm is utilized for model training, which includes the following steps:

1. **Data Preprocessing**: Data is cleaned and transformed using the above-mentioned feature engineering techniques.
2. **Hyperparameter Tuning**: The hyperparameters of the CatBoost classifier are optimized using **Optuna** to achieve the best performance.

## Project Structure

```plaintext
|-- app
|   |-- main.py                # FastAPI application
|   |-- test_main.py           # Tests for the FastAPI application
|
|-- model
|   |-- train_model.py         # Model training script
|   |-- catboost_model.pkl     # Trained model file
|
|-- data
|   |-- dataset.csv            # Input dataset
|
|-- Dockerfile                 # Dockerfile for containerizing the app
|-- requirements.txt           # Python dependencies
|-- main.yml                   # GitHub Actions CI/CD pipeline configuration
|-- README.md                  # Project documentation

### Data Preprocessing
Scripts dedicated to comprehensive data preprocessing tasks, including:
- Feature engineering for enhanced predictive power
- Data splitting using Stratified K-Fold cross-validation for training and validation sets

### Model Training and Evaluation
Utilization of the CatBoost classifier with Optuna for:
- Hyperparameter optimization to maximize model performance
- Rigorous evaluation of model efficacy and metrics

### API Development
Development of a FastAPI application:
- Designed to serve the trained model
- Enables real-time predictions based on input data
- Includes validation steps for input data integrity

### Deployment
Streamlined deployment pipeline:
- Dockerfile provided for containerizing the application
- Integration with GitHub Actions for Continuous Integration/Continuous Deployment (CI/CD)
- Deployment orchestration on Google Cloud Run for scalable and efficient model serving

## Deployment

#### Local Development, Docker Containerization, and CI/CD

1. **Local Development and Docker Build**:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   uvicorn app.main:app --reload

### Docker Deployment

1. **Build Docker Image**:
   ```bash
   docker build -t your-image-name .

2. **Run Docker Container Locally**:
   ```bash
   docker run -p 8080:8080 your-image-name

### Google Cloud Run Deployment

1. **Build and push the container image:**:
   ```bash
   gcloud auth configure-docker us-central1-docker.pkg.dev
   docker build -t us-central1-docker.pkg.dev/${PROJECT_ID}/fastapi/your_image_name:your_tag .
   docker push us-central1-docker.pkg.dev/${PROJECT_ID}/fastapi/your_image_name:your_tag

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy fastapi \
     --image=us-central1-docker.pkg.dev/${PROJECT_ID}/fastapi/your_image_name:your_tag \
     --allow-unauthenticated \
     --port=8000 \
     --service-account=${SERVICE_ACCOUNT} \
     --max-instances=10 \
     --region=us-central1 \
     --project=${PROJECT_ID}

## CI/CD Pipeline

This project uses GitHub Actions for CI/CD. The **main.yml** file in the **.github/workflows** directory defines two jobs:

- **Build and Test**: Checks out the repository, sets up Python, installs dependencies, and runs tests using pytest.
- **Deploy**: Builds and pushes the Docker image to Google Container Registry and deploys the image to Google Cloud Run.

## Usage

1. **API Endpoints**:

- **GET**: Returns a welcome message.
- **POST /predict**: Takes input data and returns a prediction of the sleep disorder.
   
2. **Example Request**:

{
  "Person_ID": 1,
  "Gender": "Male",
  "Age": 27,
  "Occupation": "Software Engineer",
  "Sleep_Duration": 6.1,
  "Quality_of_Sleep": 6,
  "Physical_Activity_Level": 42,
  "Stress_Level": 6,
  "BMI_Category": "Overweight",
  "Blood_Pressure": "126/83",
  "Heart_Rate": 77,
  "Daily_Steps": 4200
}

## License
This project is licensed under the MIT License - see the LICENSE file for details.
   
