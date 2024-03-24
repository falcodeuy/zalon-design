FROM python:3.11

WORKDIR /code

# Allows docker to cache installed dependencies and apply migrations between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . .

EXPOSE 8000

# Run the development server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]