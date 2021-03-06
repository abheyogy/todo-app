FROM python:3.9-buster

RUN pip install flask

# Copy the code to the container
COPY todo_app.py .

# Expose port 5000.
EXPOSE 50000
# Test

CMD ["python", "todo_app.py"]
