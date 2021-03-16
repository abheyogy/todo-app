FROM python:3.9-buster

RUN pip install flask

COPY todo_app.py .

EXPOSE 5000

CMD ["python", "todo_app.py"]
