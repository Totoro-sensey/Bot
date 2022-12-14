FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENTRYPOINT ["python"]
CMD ["app.py", "--host=0.0.0.0"]
