# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the password-service will run on
EXPOSE 5002

# Set the default command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
