FROM python:3.9.18

RUN mkdir /app  

WORKDIR /app 

COPY requirements.txt main.py best_catboost_model_pipeline.pkl /app/

RUN pip install update pip && pip install -r requirements.txt 

CMD [ "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000" ] 
