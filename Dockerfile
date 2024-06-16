FROM python:3.11.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 6000

CMD ["python3", "main.py"]