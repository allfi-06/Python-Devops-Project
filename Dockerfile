#Use a slim Python image as a base
FROM python:3.11-slim

#Set the working directory inside the container
WORKDIR /app

#Copy requirements file into container
COPY requirements.txt .

#Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy rest application code into container
COPY . .

#Expose the port app runs on
EXPOSE 5000

#Define command to run your application
CMD ["python","app.py"]