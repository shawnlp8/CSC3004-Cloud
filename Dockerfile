FROM python:3.8

# Make directory for application
WORKDIR /Flask

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY /Flask .

# Run applicaiton
CMD ["python", "app.py"]