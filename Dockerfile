FROM python:3.9.18

# Create a directory named 'code' and set it as the working directory
RUN mkdir /app  
WORKDIR /app 

# Copy all files from the current directory to the 'code' directory in the container
COPY . . 

# Install dependencies
RUN pip install update pip && pip install -r requirements.txt 

# Define the command to run the application using Uvicorn
CMD [ "uvicorn", "main:app", "--host=0.0.0.0", "--port=8000" ] 
