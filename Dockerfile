FROM python:3.7

WORKDIR /app

COPY lambda_sns_function/lambda_sns_function.py .
COPY lambda_sns_function/requirements.txt .
COPY lambda_sns_function/init.sql .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "sleep 10 && python lambda_sns_function.py"]
