FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3-pip libpango-1.0-0 libpangocairo-1.0-0

COPY . .

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]