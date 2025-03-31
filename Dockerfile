# Use Python 3.9.7 base image
FROM python:3.9.7

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies without caching
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from the local directory to the container
COPY . .

# Command to run the application (modify as needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
