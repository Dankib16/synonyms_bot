FROM python:3.8

COPY . /app/

WORKDIR /app/

RUN pip3 install -r requirements.txt

CMD ["python", "/app/main.py"]