# Dockerfile
FROM python:3.9.17-bookworm

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set up the application directory
ENV APP_HOME /back-end
WORKDIR $APP_HOME

# Copy all files
COPY . ./

# Explicitly copy FAISS index
COPY faiss_index /back-end/faiss_index

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
